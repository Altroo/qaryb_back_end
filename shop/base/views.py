from os import remove
from celery import current_app
from django.core.exceptions import SuspiciousFileOperation
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.base.utils import unique_slugify
from shop.base.serializers import BaseShopSerializer, BaseShopAvatarPutSerializer, \
    BaseShopNamePutSerializer, BaseShopBioPutSerializer, BaseShopAvailabilityPutSerializer, \
    BaseShopContactPutSerializer, BaseShopAddressPutSerializer, BaseShopColorPutSerializer, \
    BaseShopFontPutSerializer, BaseGETShopInfoSerializer, BaseShopPhoneContactPutSerializer, \
    BaseShopAskForCreatorLabelSerializer, \
    BaseShopModeVacanceSerializer, BaseShopModeVacancePUTSerializer
from shop.models import AuthShop, AuthShopDays, AskForCreatorLabel, PhoneCodes
from os import path
from datetime import datetime, date
import qrcode
from PIL import Image, ImageDraw, ImageFont
import qrcode.image.svg
from io import BytesIO
from shop.base.utils import ImageProcessor
import textwrap
import arabic_reshaper
from bidi.algorithm import get_display
from shop.base.tasks import base_generate_avatar_thumbnail, base_delete_mode_vacance_obj


class ShopView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        shop_name = request.data.get('shop_name')
        avatar = request.data.get('avatar')
        color_code = request.data.get('color_code')
        bg_color_code = request.data.get('bg_color_code')
        border = request.data.get('border')
        icon_color = request.data.get('icon_color')
        font_name = request.data.get('font_name')
        # unique_id = uuid4()
        # # Temp shop
        # if user.is_anonymous:
        #     serializer = BaseTempShopSerializer(data={
        #         'shop_name': shop_name,
        #         'avatar': avatar,
        #         'color_code': color_code,
        #         'bg_color_code': bg_color_code,
        #         'border': border,
        #         'icon_color': icon_color,
        #         'font_name': font_name,
        #         'unique_id': str(unique_id),
        #     })
        #     if serializer.is_valid():
        #         auth_shop = serializer.save()
        #         qaryb_link = unique_slugify(instance=auth_shop,
        #         value=auth_shop.shop_name, slug_field_name='qaryb_link')
        #         auth_shop.qaryb_link = qaryb_link
        #         auth_shop.save()
        #         # shift = datetime.utcnow() + timedelta(hours=24)
        #         shift = datetime.utcnow() + timedelta(days=60)
        #         data = {
        #             'unique_id': unique_id,
        #             'shop_name': auth_shop.shop_name,
        #             'avatar': auth_shop.get_absolute_avatar_img,
        #             'color_code': auth_shop.color_code,
        #             'bg_color_code': auth_shop.bg_color_code,
        #             'border': auth_shop.border,
        #             'icon_color': auth_shop.icon_color,
        #             'font_name': auth_shop.font_name,
        #             'qaryb_link': qaryb_link,
        #             'expiration_date': shift
        #         }
        #         # Generate thumbnail
        #         base_generate_avatar_thumbnail.apply_async((auth_shop.pk, 'TempShop'), )
        #         task_id = base_start_deleting_expired_shops.apply_async((auth_shop.pk,), eta=shift)
        #         auth_shop.task_id = str(task_id)
        #         auth_shop.save()
        #         return Response(data=data, status=status.HTTP_200_OK)
        #     raise ValidationError(serializer.errors)
        # Auth shop
        # else:
        serializer = BaseShopSerializer(data={
            'user': user.pk,
            'shop_name': shop_name,
            'avatar': avatar,
            'color_code': color_code,
            'bg_color_code': bg_color_code,
            'border': border,
            'icon_color': icon_color,
            'font_name': font_name,
            'creator': False,
        })
        if serializer.is_valid():
            shop = serializer.save()
            qaryb_link = unique_slugify(instance=shop, value=shop.shop_name, slug_field_name='qaryb_link')
            shop.qaryb_link = qaryb_link
            shop.save()
            data = {
                'pk': shop.pk,
                'shop_name': shop.shop_name,
                'avatar': shop.get_absolute_avatar_img,
                'color_code': shop.color_code,
                'bg_color_code': shop.bg_color_code,
                'border': shop.border,
                'icon_color': shop.icon_color,
                'font_name': shop.font_name,
                'creator': False,
                'qaryb_link': qaryb_link
            }
            # Generate thumbnail
            base_generate_avatar_thumbnail.apply_async((shop.pk, 'AuthShop'), )
            return Response(data=data, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors)

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = kwargs.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             shop_details_serializer = BaseGETTempShopInfoSerializer(auth_shop)
        #             return Response(shop_details_serializer.data, status=status.HTTP_200_OK)
        #         except TempShop.DoesNotExist:
        #             data = {"errors": ["Shop not found."]}
        #             raise ValidationError(data)
        #     else:
        #         shop_link = kwargs.get('shop_link')
        #         if shop_link:
        #             auth_shop = AuthShop.objects.get(qaryb_link=shop_link)
        #             shop_details_serializer = BaseGETShopInfoSerializer(auth_shop)
        #             return Response(shop_details_serializer.data, status=status.HTTP_200_OK)
        #         data = {"errors": ["Shop not found."]}
        #         raise ValidationError(data)
        # # Auth shop
        # else:
        shop_link = kwargs.get('shop_link')
        try:
            if shop_link:
                auth_shop = AuthShop.objects.get(qaryb_link=shop_link)
            else:
                auth_shop = AuthShop.objects.get(user=user)
            shop_details_serializer = BaseGETShopInfoSerializer(auth_shop)
            return Response(shop_details_serializer.data, status=status.HTTP_200_OK)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopAvatarPutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopAvatarPutSerializer(auth_shop, data=request.data, partial=True)
        #             if serializer.is_valid():
        #                 if auth_shop.avatar:
        #                     try:
        #                         remove(auth_shop.avatar.path)
        #                     except (ValueError, SuspiciousFileOperation, FileNotFoundError):
        #                         pass
        #                 if auth_shop.avatar_thumbnail:
        #                     try:
        #                         remove(auth_shop.avatar_thumbnail.path)
        #                     except (ValueError, SuspiciousFileOperation, FileNotFoundError):
        #                         pass
        #                 # new_avatar = serializer.update(temp_shop, serializer.validated_data)
        #                 new_avatar = serializer.save()
        #                 # Generate new avatar thumbnail
        #                 base_generate_avatar_thumbnail.apply_async((new_avatar.pk, 'TempShop'), )
        #                 data = {
        #                     'avatar': auth_shop.get_absolute_avatar_img,
        #                 }
        #                 return Response(data=data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopAvatarPutSerializer(shop, data=request.data, partial=True)
            if serializer.is_valid():
                if shop.avatar:
                    try:
                        remove(shop.avatar.path)
                    except (ValueError, SuspiciousFileOperation, FileNotFoundError):
                        pass
                if shop.avatar_thumbnail:
                    try:
                        remove(shop.avatar_thumbnail.path)
                    except (ValueError, SuspiciousFileOperation, FileNotFoundError):
                        pass
                # new_avatar = serializer.update(shop, serializer.validated_data)
                new_avatar = serializer.save()
                # Generate new avatar thumbnail
                base_generate_avatar_thumbnail.apply_async((new_avatar.pk, 'AuthShop'), )
                data = {
                    'avatar': shop.get_absolute_avatar_img,
                }
                return Response(data=data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopNamePutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopNamePutSerializer(auth_shop, data=request.data, partial=True)
        #             if serializer.is_valid():
        #                 # serializer.update(temp_shop, serializer.validated_data)
        #                 serializer.save()
        #                 return Response(data=serializer.data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopNamePutSerializer(shop, data=request.data, partial=True)
            if serializer.is_valid():
                # serializer.update(shop, serializer.validated_data)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopBioPutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopBioPutSerializer(auth_shop, data=request.data, partial=True)
        #             if serializer.is_valid():
        #                 # serializer.update(temp_shop, serializer.validated_data)
        #                 serializer.save()
        #                 return Response(data=serializer.data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopBioPutSerializer(shop, data=request.data, partial=True)
            if serializer.is_valid():
                # serializer.update(shop, serializer.validated_data)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopAvailabilityPutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        morning_hour_from = request.data.get('morning_hour_from', '')
        morning_hour_to = request.data.get('morning_hour_to', '')
        afternoon_hour_from = request.data.get('afternoon_hour_from', '')
        afternoon_hour_to = request.data.get('afternoon_hour_to', '')
        opening_days = str(request.data.get('opening_days')).split(',')
        opening_days = AuthShopDays.objects.filter(code_day__in=opening_days)
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopAvailabilityPutSerializer(auth_shop, data={
        #                 'morning_hour_from': morning_hour_from,
        #                 'morning_hour_to': morning_hour_to,
        #                 'afternoon_hour_from': afternoon_hour_from,
        #                 'afternoon_hour_to': afternoon_hour_to,
        #             }, partial=True)
        #             if serializer.is_valid():
        #                 # new_availability = serializer.update(temp_shop, serializer.validated_data)
        #                 new_availability = serializer.save()
        #                 new_availability.opening_days.clear()
        #                 days_list = []
        #                 for day in opening_days:
        #                     new_availability.opening_days.add(day.pk)
        #                     days_list.append({
        #                         'pk': day.pk,
        #                         'code_day': day.code_day,
        #                         'name_day': day.name_day
        #                     })
        #                 data = {
        #                     'opening_days': days_list,
        #                     'morning_hour_from': serializer.data.get('morning_hour_from'),
        #                     'morning_hour_to': serializer.data.get('morning_hour_to'),
        #                     'afternoon_hour_from': serializer.data.get('afternoon_hour_from'),
        #                     'afternoon_hour_to': serializer.data.get('afternoon_hour_to'),
        #                 }
        #                 return Response(data=data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopAvailabilityPutSerializer(shop, data={
                'morning_hour_from': morning_hour_from,
                'morning_hour_to': morning_hour_to,
                'afternoon_hour_from': afternoon_hour_from,
                'afternoon_hour_to': afternoon_hour_to,
            }, partial=True)
            if serializer.is_valid():
                # new_availability = serializer.update(shop, serializer.validated_data)
                new_availability = serializer.save()
                new_availability.opening_days.clear()
                days_list = []
                for day in opening_days:
                    new_availability.opening_days.add(day.pk)
                    days_list.append({
                        'pk': day.pk,
                        'code_day': day.code_day,
                        'name_day': day.name_day
                    })
                data = {
                    'opening_days': days_list,
                    'morning_hour_from': serializer.data.get('morning_hour_from'),
                    'morning_hour_to': serializer.data.get('morning_hour_to'),
                    'afternoon_hour_from': serializer.data.get('afternoon_hour_from'),
                    'afternoon_hour_to': serializer.data.get('afternoon_hour_to'),
                }
                return Response(data=data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopContactPutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopContactPutSerializer(auth_shop, data=request.data, partial=True)
        #             if serializer.is_valid():
        #                 # serializer.update(temp_shop, serializer.validated_data)
        #                 serializer.save()
        #                 return Response(data=serializer.data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopContactPutSerializer(shop, data=request.data, partial=True)
            if serializer.is_valid():
                # serializer.update(shop, serializer.validated_data)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopPhoneContactPutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopPhoneContactPutSerializer(auth_shop, data=request.data, partial=True)
        #             if serializer.is_valid():
        #                 # serializer.update(temp_shop, serializer.validated_data)
        #                 serializer.save()
        #                 return Response(data=serializer.data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopPhoneContactPutSerializer(shop, data=request.data, partial=True)
            if serializer.is_valid():
                # serializer.update(shop, serializer.validated_data)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopAddressPutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopAddressPutSerializer(auth_shop, data=request.data, partial=True)
        #             if serializer.is_valid():
        #                 # serializer.update(temp_shop, serializer.validated_data)
        #                 serializer.save()
        #                 return Response(data=serializer.data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopAddressPutSerializer(shop, data=request.data, partial=True)
            if serializer.is_valid():
                # serializer.update(shop, serializer.validated_data)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopColorPutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopColorPutSerializer(auth_shop, data=request.data, partial=True)
        #             if serializer.is_valid():
        #                 # serializer.update(temp_shop, serializer.validated_data)
        #                 serializer.save()
        #                 return Response(data=serializer.data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopColorPutSerializer(shop, data=request.data, partial=True)
            if serializer.is_valid():
                # serializer.update(shop, serializer.validated_data)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopFontPutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        # # Temp shop
        # if user.is_anonymous:
        #     unique_id = request.data.get('unique_id')
        #     if unique_id:
        #         try:
        #             auth_shop = TempShop.objects.get(unique_id=unique_id)
        #             serializer = BaseTempShopFontPutSerializer(auth_shop, data=request.data, partial=True)
        #             if serializer.is_valid():
        #                 # serializer.update(temp_shop, serializer.validated_data)
        #                 serializer.save()
        #                 return Response(data=serializer.data, status=status.HTTP_200_OK)
        #             raise ValidationError(serializer.errors)
        #         except TempShop.DoesNotExist:
        #             errors = {"errors": ["Shop not found."]}
        #             raise ValidationError(errors)
        #     data = {"errors": ["Shop not found."]}
        #     raise ValidationError(data)
        # # Auth shop
        # else:
        try:
            shop = AuthShop.objects.get(user=user)
            serializer = BaseShopFontPutSerializer(shop, data=request.data, partial=True)
            if serializer.is_valid():
                # serializer.update(shop, serializer.validated_data)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


# class TempShopToAuthShopView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     @staticmethod
#     def post(request, *args, **kwargs):
#         unique_id = request.data.get('unique_id')
#         user = request.user
#         try:
#             temp_shop = TempShop.objects.get(unique_id=unique_id)
#             # transfer temp shop data
#             try:
#                 auth_shop = AuthShop.objects.create(
#                     user=user,
#                     shop_name=temp_shop.shop_name,
#                     avatar=temp_shop.avatar,
#                     avatar_thumbnail=temp_shop.avatar_thumbnail,
#                     color_code=temp_shop.color_code,
#                     bg_color_code=temp_shop.bg_color_code,
#                     border=temp_shop.border,
#                     icon_color=temp_shop.icon_color,
#                     font_name=temp_shop.font_name,
#                     bio=temp_shop.bio,
#                     morning_hour_from=temp_shop.morning_hour_from,
#                     morning_hour_to=temp_shop.morning_hour_to,
#                     afternoon_hour_from=temp_shop.afternoon_hour_from,
#                     afternoon_hour_to=temp_shop.afternoon_hour_to,
#                     contact_phone_code=temp_shop.contact_phone_code,
#                     contact_phone=temp_shop.contact_phone,
#                     contact_whatsapp_code=temp_shop.contact_whatsapp_code,
#                     contact_whatsapp=temp_shop.contact_whatsapp,
#                     contact_mode=temp_shop.contact_mode,
#                     phone=temp_shop.phone,
#                     contact_email=temp_shop.contact_email,
#                     website_link=temp_shop.website_link,
#                     facebook_link=temp_shop.facebook_link,
#                     twitter_link=temp_shop.twitter_link,
#                     instagram_link=temp_shop.instagram_link,
#                     whatsapp=temp_shop.whatsapp,
#                     zone_by=temp_shop.zone_by,
#                     longitude=temp_shop.longitude,
#                     latitude=temp_shop.latitude,
#                     address_name=temp_shop.address_name,
#                     km_radius=temp_shop.km_radius,
#                     qaryb_link=temp_shop.qaryb_link,
#                 )
#                 auth_shop.save()
#                 # revoke 24h periodic task
#                 task_id = temp_shop.task_id
#                 current_app.control.revoke(task_id, terminate=True, signal='SIGKILL')
#                 temp_shop.task_id = None
#                 temp_shop.save()
#                 # Auth shop opening days
#                 opening_days = temp_shop.opening_days.all()
#                 for opening_day in opening_days:
#                     auth_shop.opening_days.add(opening_day.pk)
#                 # Offers
#                 temp_offers = TempOffers.objects.filter(auth_shop=temp_shop.pk) \
#                     .select_related('temp_offer_products') \
#                     .select_related('temp_offer_services') \
#                     .select_related('temp_offer_solder') \
#                     .prefetch_related('temp_offer_delivery')
#                 for temp_offer in temp_offers:
#                     offer = Offers.objects.create(
#                         auth_shop=auth_shop,
#                         offer_type=temp_offer.offer_type,
#                         # Offer categories
#                         title=temp_offer.title,
#                         # May lead to a db error picture not found (we'll see)
#                         picture_1=temp_offer.picture_1,
#                         picture_2=temp_offer.picture_2,
#                         picture_3=temp_offer.picture_3,
#                         picture_4=temp_offer.picture_4,
#                         picture_1_thumbnail=temp_offer.picture_1_thumbnail,
#                         picture_2_thumbnail=temp_offer.picture_2_thumbnail,
#                         picture_3_thumbnail=temp_offer.picture_3_thumbnail,
#                         picture_4_thumbnail=temp_offer.picture_4_thumbnail,
#                         description=temp_offer.description,
#                         # For whom
#                         # Tags
#                         made_in_label=temp_offer.made_in_label,
#                         price=temp_offer.price,
#                     )
#                     offer.save()
#                     temp_categories = temp_offer.offer_categories.all()
#                     for temp_categorie in temp_categories:
#                         offer.offer_categories.add(temp_categorie.pk)
#                     for_whoms = temp_offer.for_whom.all()
#                     for for_whom in for_whoms:
#                         offer.for_whom.add(for_whom.pk)
#                     tags = temp_offer.tags.all()
#                     for tag in tags:
#                         offer.tags.add(tag.pk)
#                     if temp_offer.offer_type == 'V':
#                         product = Products.objects.create(
#                             offer=offer,
#                             # product_colors
#                             # product_sizes
#                             product_quantity=temp_offer.temp_offer_products.product_quantity,
#                             product_price_by=temp_offer.temp_offer_products.product_price_by,
#                             product_longitude=temp_offer.temp_offer_products.product_longitude,
#                             product_latitude=temp_offer.temp_offer_products.product_latitude,
#                             product_address=temp_offer.temp_offer_products.product_address
#                         )
#                         product.save()
#                         # product_colors
#                         product_colors = temp_offer.temp_offer_products.product_colors.all()
#                         for product_color in product_colors:
#                             product.product_colors.add(product_color.pk)
#                         # product_sizes
#                         product_sizes = temp_offer.temp_offer_products.product_sizes.all()
#                         for product_size in product_sizes:
#                             product.product_sizes.add(product_size.pk)
#                     elif temp_offer.offer_type == 'S':
#                         service = Services.objects.create(
#                             offer=offer,
#                             # service_availability_days
#                             service_morning_hour_from=temp_offer.temp_offer_services.service_morning_hour_from,
#                             service_morning_hour_to=temp_offer.temp_offer_services.service_morning_hour_to,
#                             service_afternoon_hour_from=temp_offer.temp_offer_services.service_afternoon_hour_from,
#                             service_afternoon_hour_to=temp_offer.temp_offer_services.service_afternoon_hour_to,
#                             service_zone_by=temp_offer.temp_offer_services.service_zone_by,
#                             service_price_by=temp_offer.temp_offer_services.service_price_by,
#                             service_longitude=temp_offer.temp_offer_services.service_longitude,
#                             service_latitude=temp_offer.temp_offer_services.service_latitude,
#                             service_address=temp_offer.temp_offer_services.service_address,
#                             service_km_radius=temp_offer.temp_offer_services.service_km_radius
#                         )
#                         service.save()
#                         # service_availability_days
#                         service_availability_days = temp_offer.temp_offer_services.service_availability_days.all()
#                         for service_availability_day in service_availability_days:
#                             service.service_availability_days.add(service_availability_day.pk)
#                     # Transfer solder
#                     try:
#                         temp_solder = TempSolder.objects.get(offer=temp_offer.pk)
#                         solder = Solder.objects.create(
#                             offer=offer.pk,
#                             solder_type=temp_solder.solder_type,
#                             solder_value=temp_solder.solder_value
#                         )
#                         solder.save()
#                     except TempSolder.DoesNotExist:
#                         pass
#                     # Transfer deliveries
#                     temp_deliveries = TempDelivery.objects.filter(offer=temp_offer.pk)
#                     for temp_delivery in temp_deliveries:
#                         delivery = Delivery.objects.create(
#                             offer=offer.pk,
#                             # delivery_city
#                             all_cities=temp_delivery.all_cities,
#                             delivery_price=temp_delivery.delivery_price,
#                             delivery_days=temp_delivery.delivery_days,
#                         )
#                         delivery.save()
#                         temp_delivery_cities = temp_delivery.delivery_city.all()
#                         for temp_delivery_city in temp_delivery_cities:
#                             delivery.delivery_city.add(temp_delivery_city.pk)
#                 temp_shop.delete()
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#             except IntegrityError:
#                 errors = {"errors": ["You already own a shop."]}
#                 raise ValidationError(errors)
#         except TempShop.DoesNotExist:
#             errors = {"errors": ["Shop not found."]}
#             raise ValidationError(errors)


class ShopAskBecomeCreator(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        try:
            auth_shop = AuthShop.objects.get(user=user)
            try:
                ask_for_creator = AskForCreatorLabel.objects.get(auth_shop=auth_shop)
                ask_for_creator.asked_counter = ask_for_creator.asked_counter + 1
                ask_for_creator.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except AskForCreatorLabel.DoesNotExist:
                serializer = BaseShopAskForCreatorLabelSerializer(data={
                    'auth_shop': auth_shop.pk,
                })
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopQrCodeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parent_file_dir = path.abspath(path.join(path.dirname(__file__), "../.."))

    @staticmethod
    def from_img_to_io(image, format_, type_):
        if type_ == 'input':
            image = Image.fromarray(image)
        # type == 'output'
        bytes_io = BytesIO()
        image.save(bytes_io, format=format_)
        bytes_io.seek(0)
        return bytes_io

    @staticmethod
    def get_text_fill_color(bg_color):
        # white 255, 255, 255
        # black 0, 0, 0
        match bg_color:
            case ("#F3DCDC" | "#FFD9A2" | "#F8F2DA" | "#DBF4EA" | "#DBE8F4" | "#D5CEEE" | "#F3D8E1" | "#EBD2AD"
                  | "#E2E4E2" | "#FFFFFF" | "#FFA826" | "#FED301" | "#07CBAD" | "#FF9DBF" | "#CEB186"):
                return 0, 0, 0
            case ("#FF5D6B" | "#0274D7" | "#8669FB" | "#878E88" | "#0D070B"):
                return 255, 255, 255
            case _:
                # Return black color as default
                return 0, 0, 0

    def post(self, request, *args, **kwargs):
        user = request.user
        bg_color = request.data.get('bg_color')
        qr_text = request.data.get('qr_text')
        if len(str(qr_text)) > 60:
            errors = {"qr_text": ["Qr code text should be less than 60 characters."]}
            raise ValidationError(errors)
        try:
            auth_shop = AuthShop.objects.get(user=user)
            qaryb_link = auth_shop.qaryb_link
            icon_path = self.parent_file_dir + '/static/icons/qaryb_icon_300_300.png'
            image_processor = ImageProcessor()
            loaded_img = image_processor.load_image(icon_path)
            resized_img = image_processor.image_resize(loaded_img, width=1000, height=1000)
            img_thumbnail = self.from_img_to_io(resized_img, 'PNG', 'input')
            logo = Image.open(img_thumbnail)
            basewidth = 100
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            qr_code = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=10,
            )
            qr_code.add_data(qaryb_link)
            qr_code.make(fit=True)
            qr_img = qr_code.make_image(fill_color='Black', back_color='white').convert('RGBA')
            pos = ((qr_img.size[0] - logo.size[0]) // 2,
                   (qr_img.size[1] - logo.size[1]) // 2)
            qr_img.paste(logo, pos)
            max_w, max_h = qr_img.size[0] - qr_code.box_size ** 2 - qr_code.border ** 2, 60
            color_box = Image.new("RGB", (max_w, max_h), color='white')
            drawn_text_img = ImageDraw.Draw(color_box)
            drawn_text_img.rounded_rectangle(((0, 0), (max_w, max_h)), 20, fill=bg_color)
            unicode_text_reshaped = arabic_reshaper.reshape(qr_text)
            para = textwrap.wrap(unicode_text_reshaped, width=35)
            para = '\n'.join(para)
            unicode_text_reshaped_rtl = get_display(para, base_dir='R')
            unicode_font = ImageFont.truetype(self.parent_file_dir + '/static/fonts/Changa-Regular.ttf', 20)
            fill = self.get_text_fill_color(bg_color)
            text_width, text_height = drawn_text_img.textsize(unicode_text_reshaped_rtl, font=unicode_font)
            drawn_text_img.text(((max_w - text_width) / 2, (max_h - text_height - 10) / 2), unicode_text_reshaped_rtl,
                                align='center', font=unicode_font,
                                fill=fill)
            pos_for_text = ((qr_img.size[0] - drawn_text_img._image.width) // 2,
                            (qr_img.size[1] - drawn_text_img._image.height - 20))
            qr_img.paste(drawn_text_img._image, pos_for_text)
            qr_code_img = self.from_img_to_io(qr_img, 'PNG', 'output')
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Delete old qr code before generating new one
            try:
                old_qr_code_img = auth_shop.qr_code_img.path
                remove(old_qr_code_img)
            except (FileNotFoundError, ValueError, AttributeError):
                pass
            auth_shop.save_qr_code('qr_code_img', qr_code_img, uid)
            qr_code_img = AuthShop.objects.get(user=user).get_absolute_qr_code_img
            data = {
                'qr_code': qr_code_img
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["User doesn't own a shop yet."]}
            raise ValidationError(errors)

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        try:
            qr_code_img = AuthShop.objects.get(user=user).get_absolute_qr_code_img
            data = {
                'qr_code': qr_code_img
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopVisitCardView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        try:
            auth_shop = AuthShop.objects.get(user=user)
            data = {
                'avatar': auth_shop.get_absolute_avatar_thumbnail,
                'shop_name': auth_shop.shop_name,
                'user_first_name': auth_shop.user.first_name,
                'user_last_name': auth_shop.user.last_name,
                'shop_link': auth_shop.qaryb_link,
                'phone': auth_shop.phone,
                'contact_email': auth_shop.contact_email,
                'facebook_link': auth_shop.facebook_link,
                'instagram_link': auth_shop.instagram_link,
                'whatsapp': auth_shop.whatsapp,
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopModeVacanceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        try:
            auth_shop = AuthShop.objects.select_related('auth_shop_mode_vacance').get(user=user)
            try:
                mode_vacance_serializer = BaseShopModeVacanceSerializer(auth_shop.auth_shop_mode_vacance)
                return Response(data=mode_vacance_serializer.data, status=status.HTTP_200_OK)
            except auth_shop.auth_shop_mode_vacance.DoesNotExist:
                return Response(data={}, status=status.HTTP_200_OK)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        try:
            auth_shop = AuthShop.objects.get(user=user)
            date_from = datetime.strptime(request.data.get('date_from'), '%Y-%m-%d')
            date_to = datetime.strptime(request.data.get('date_to'), '%Y-%m-%d')
            if date_from > date_to:
                errors = {"errors": ["Date from is > than date to."]}
                raise ValidationError(errors)
            else:
                serializer = BaseShopModeVacanceSerializer(data={
                    'auth_shop': auth_shop.pk,
                    'date_from': request.data.get('date_from'),
                    'date_to': request.data.get('date_to'),
                })
                if serializer.is_valid():
                    mode_vacance = serializer.save()
                    mode_vacance.save()
                    # Generate new periodic task
                    today_date = date.today()
                    mode_vacance_to = mode_vacance.date_to
                    days_left = mode_vacance_to - today_date
                    shift = datetime.utcnow() + days_left
                    mode_vacance_task_id = base_delete_mode_vacance_obj.apply_async((mode_vacance.pk,), eta=shift)
                    auth_shop.mode_vacance_task_id = str(mode_vacance_task_id)
                    auth_shop.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                raise ValidationError(serializer.errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)

    @staticmethod
    def delete(request, *args, **kwargs):
        user = request.user
        try:
            auth_shop = AuthShop.objects.select_related('auth_shop_mode_vacance').get(user=user)
            try:
                auth_shop.auth_shop_mode_vacance.delete()
                # revoke mode vacance periodic task
                mode_vacance_task_id = auth_shop.mode_vacance_task_id
                current_app.control.revoke(mode_vacance_task_id, terminate=True, signal='SIGKILL')
                auth_shop.mode_vacance_task_id = None
                auth_shop.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except auth_shop.auth_shop_mode_vacance.DoesNotExist:
                errors = {"errors": ["Mode vacance not found."]}
                raise ValidationError(errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)

    @staticmethod
    def patch(request, *args, **kwargs):
        user = request.user
        try:
            auth_shop = AuthShop.objects.select_related('auth_shop_mode_vacance').get(user=user)
            try:
                date_from = datetime.strptime(request.data.get('date_from'), '%Y-%m-%d')
                date_to = datetime.strptime(request.data.get('date_to'), '%Y-%m-%d')
                if date_from > date_to:
                    errors = {"errors": ["Date from is > than date to."]}
                    raise ValidationError(errors)
                else:
                    serializer = BaseShopModeVacancePUTSerializer(auth_shop.auth_shop_mode_vacance,
                                                                  data=request.data, partial=True)
                    if serializer.is_valid():
                        # serializer.update(auth_shop.auth_shop_mode_vacance, serializer.validated_data)
                        serializer.save()
                        # revoke previous mode vacance periodic task
                        mode_vacance_task_id = auth_shop.mode_vacance_task_id
                        current_app.control.revoke(mode_vacance_task_id, terminate=True, signal='SIGKILL')
                        auth_shop.mode_vacance_task_id = None
                        auth_shop.save()
                        # Generate new periodic task
                        today_date = date.today()
                        mode_vacance_to = serializer.validated_data.get('date_to')
                        days_left = mode_vacance_to - today_date
                        shift = datetime.utcnow() + days_left
                        mode_vacance_task_id = base_delete_mode_vacance_obj.apply_async(
                            (serializer.validated_data.get('pk'),), eta=shift)
                        auth_shop.mode_vacance_task_id = str(mode_vacance_task_id)
                        auth_shop.save()
                        return Response(data=serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except auth_shop.auth_shop_mode_vacance.DoesNotExist:
                errors = {"errors": ["Mode vacance not found."]}
                raise ValidationError(errors)
        except AuthShop.DoesNotExist:
            errors = {"errors": ["Shop not found."]}
            raise ValidationError(errors)


class ShopGetPhoneCodesView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request, *args, **kwargs):
        data = {}
        phone_codes = PhoneCodes.objects.all().order_by('phone_code').values_list('phone_code', flat=True)
        data['phone_codes'] = phone_codes
        return Response(data=data, status=status.HTTP_200_OK)

#
# class ShopUniqueIDVerifyView(APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     @staticmethod
#     def post(request, *args, **kwargs):
#         unique_id = request.data.get('unique_id')
#         try:
#             TempShop.objects.get(unique_id=unique_id)
#             return Response(status=status.HTTP_200_OK)
#         except TempShop.DoesNotExist:
#             data = {
#                 "detail": "Unique_id is invalid or expired",
#                 "code": "unique_id_not_valid"
#             }
#             return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
