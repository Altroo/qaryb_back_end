from typing import Union
from django.db.models import QuerySet
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from order.models import Order
from order.base.serializers import BaseOrdersListSerializer, \
    BaseChiffreAffaireListSerializer
from order.base.filters import OrderStatusFilterSet
from notifications.models import Notifications
from order.base.tasks import base_send_order_email
from decouple import config


class ShopSellingOrdersView(ListAPIView, PageNumberPagination):
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = OrderStatusFilterSet
    serializer_class = BaseOrdersListSerializer
    http_method_names = ('get',)

    def get_queryset(self) -> Union[QuerySet, Order]:
        user = self.request.user
        return Order.objects.filter(seller__user=user) \
            .prefetch_related('order_details_order')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_queryset: QuerySet = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class ShopBuyingOrdersView(ListAPIView, PageNumberPagination):
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = OrderStatusFilterSet
    serializer_class = BaseOrdersListSerializer
    http_method_names = ('get',)

    def get_queryset(self) -> Union[QuerySet, Order]:
        user = self.request.user
        return Order.objects.filter(buyer=user) \
            .prefetch_related('order_details_order')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_queryset: QuerySet = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class GetOrderDetailsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        order_pk = kwargs.get('order_pk')
        sell_order = Order.objects.filter(seller__user=user, pk=order_pk)
        buy_order = Order.objects.filter(buyer=user, pk=order_pk)
        if sell_order:
            serializer = BaseOrdersListSerializer(instance=sell_order[0],
                                                  context={'order_for': 'S'})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if buy_order:
            serializer = BaseOrdersListSerializer(instance=buy_order[0],
                                                  context={'order_for': 'B'})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if not sell_order or not buy_order:
            errors = {"errors": ["Order Doesn't exist!"]}
            raise ValidationError(errors)

    @staticmethod
    def get_offer_total_price(instance, offer_type):
        offer_price = instance.offer_price
        if offer_type == 'V':
            if instance.picked_quantity:
                return offer_price * instance.picked_quantity
            else:
                return offer_price
        else:
            return offer_price


class CancelAllView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        order_pk = request.data.get('order_pk')
        sell_order = Order.objects.filter(seller__user=user, pk=order_pk)
        buy_order = Order.objects.filter(buyer=user, pk=order_pk)
        mail_subject = 'Votre commande est annulée'
        if sell_order:
            sell_order[0].order_status = 'CA'
            sell_order[0].save(update_fields=['order_status'])
            # Commande annulée par le vendeur.
            mail_template = 'commande_annulee_acheteur.html'
            if sell_order[0].buyer:
                Notifications.objects.create(user=sell_order[0].buyer, type='CS')
                email = sell_order[0].buyer.email
                first_name = sell_order[0].buyer.first_name
                shop_name = sell_order[0].seller.shop_name
                href = f'{config("FRONT_DOMAIN")}$/dashboard/my-business/orders/{order_pk}'
                base_send_order_email.apply_async((mail_subject, mail_template,
                                                   email, first_name, href, shop_name),)
            else:
                # Anonymous user
                email = sell_order[0].order_details_order.all()[0].email
                first_name = sell_order[0].first_name
                shop_name = sell_order[0].seller.shop_name
                base_send_order_email.apply_async((mail_subject, mail_template,
                                                   email, first_name, None, shop_name), )
            return Response(status=status.HTTP_204_NO_CONTENT)
        if buy_order:
            # Commande annulée par l'acheteur. (already connected)
            buy_order[0].order_status = 'CA'
            buy_order[0].save(update_fields=['order_status'])
            Notifications.objects.create(user=buy_order[0].seller.user, type='CA')
            mail_template = 'commande_annulee_vendeur.html'
            email = sell_order[0].seller.email
            first_name = sell_order[0].seller.first_name
            href = f'{config("FRONT_DOMAIN")}/dashboard/my-business/orders/{order_pk}'
            base_send_order_email.apply_async((mail_subject, mail_template,
                                               email, first_name, href), )
            return Response(status=status.HTTP_204_NO_CONTENT)


class AcceptOrdersView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        order_pk = request.data.get('order_pk')
        try:
            order = Order.objects.get(pk=order_pk, seller__user=user)
            order_details = order.order_details_order.all()
            # Reduce quantity of products.
            # Case offer was deleted & no longer available
            for order_detail in order_details:
                if order_detail.offer_type == 'V':
                    try:
                        product_quantity = order_detail.offer.offer_products.product_quantity
                        # Check for selected positive quantity
                        if isinstance(product_quantity, int) and product_quantity > 0:
                            product_quantity -= order_detail.picked_quantity
                            if product_quantity >= 0:
                                order_detail.offer.offer_products.product_quantity = product_quantity
                            else:
                                order_detail.offer.offer_products.product_quantity = 0
                            order_detail.offer.offer_products.save(update_fields=['product_quantity'])
                    except AttributeError:
                        pass
            if order.order_status == 'IP':
                order.order_status = 'CM'
                order.save(update_fields=['order_status'])
                mail_subject = 'Votre commande est en cours de traitement'
                mail_template = 'commande_en_traitement.html'
                if order.buyer:
                    # Votre commande à été accepté par le vendeur.
                    Notifications.objects.create(user=order.buyer, type='OA')
                    email = order.buyer.email
                    first_name = order.buyer.first_name
                    shop_name = order.seller.shop_name
                    href = f'{config("FRONT_DOMAIN")}$/dashboard/my-business/orders/{order_pk}'
                    base_send_order_email.apply_async((mail_subject, mail_template,
                                                       email, first_name, href, shop_name), )
                else:
                    email = order.order_details_order.all()[0].email
                    first_name = order.first_name
                    shop_name = order.seller.shop_name
                    base_send_order_email.apply_async((mail_subject, mail_template,
                                                       email, first_name, None, shop_name), )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            errors = {"error": ["Order doesn't exist!"]}
            raise ValidationError(errors)


class GetChiffreAffaireListView(ListAPIView, PageNumberPagination):
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = OrderStatusFilterSet
    serializer_class = BaseChiffreAffaireListSerializer
    http_method_names = ('get',)

    def get_queryset(self) -> Union[QuerySet, Order]:
        user = self.request.user
        return Order.objects.filter(seller__user=user) \
            .prefetch_related('order_details_order')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_queryset: QuerySet = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class GetNewOrdersCountView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        orders_count = Order.objects.filter(seller__user=user, order_status='CM').count()
        data = {
            'orders_count': orders_count,
        }
        return Response(data=data, status=status.HTTP_200_OK)
