from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from temp_shop.base.serializers import BaseTempShopSerializer, BaseTempShopAvatarPutSerializer, \
    BaseTempShopNamePutSerializer, BaseTempShopBioPutSerializer, BaseTempShopAvailabilityPutSerializer, \
    BaseTempShopContactPutSerializer, BaseTempShopAddressPutSerializer, BaseTempShopColorPutSerializer, \
    BaseTempShopFontPutSerializer, BaseGETTempShopInfoSerializer, BaseTempShopTelPutSerializer, \
    BaseTempShopWtspPutSerializer
from os import path, remove
from uuid import uuid4
from urllib.parse import quote_plus
from datetime import datetime, timedelta
from temp_shop.base.tasks import base_start_deleting_expired_shops
from auth_shop.base.tasks import base_generate_avatar_thumbnail
from temp_shop.base.models import TempShop, AuthShopDays
from django.core.exceptions import SuspiciousFileOperation


class TempShopView(APIView):
    permission_classes = (permissions.AllowAny,)
    parent_file_dir = path.abspath(path.join(path.dirname(__file__), "../.."))

    @staticmethod
    def post(request, *args, **kwargs):
        shop_name = request.data.get('shop_name')
        qaryb_url = quote_plus(shop_name)
        unique_id = uuid4()
        serializer = BaseTempShopSerializer(data={
            'shop_name': shop_name,
            'avatar': request.data.get('avatar'),
            'color_code': request.data.get('color_code'),
            'bg_color_code': request.data.get('bg_color_code'),
            'font_name': request.data.get('font_name'),
            # 'bio': request.data.get('bio'),
            # 'morning_hour_from': request.data.get('morning_hour_from'),
            # 'morning_hour_to': request.data.get('morning_hour_to'),
            # 'afternoon_hour_from': request.data.get('afternoon_hour_from'),
            # 'afternoon_hour_to': request.data.get('afternoon_hour_to'),
            # 'phone': request.data.get('phone'),
            # 'contact_email': request.data.get('contact_email'),
            # 'website_link': request.data.get('website_link'),
            # 'facebook_link': request.data.get('facebook_link'),
            # 'twitter_link': request.data.get('twitter_link'),
            # 'instagram_link': request.data.get('instagram_link'),
            # 'whatsapp': request.data.get('whatsapp'),
            # 'zone_by': request.data.get('zone_by'),
            # 'longitude': request.data.get('longitude'),
            # 'latitude': request.data.get('latitude'),
            # 'address_name': request.data.get('address_name'),
            # 'km_radius': request.data.get('km_radius'),
            'qaryb_link': 'https://qaryb.com/' + qaryb_url + str(unique_id),
            'unique_id': str(unique_id),
        })
        if serializer.is_valid():
            temp_shop = serializer.save()
            temp_shop.save()
            # Opening days
            # opening_days = str(request.data.get('opening_days')).split(',')
            # opening_days = Days.objects.filter(code_day__in=opening_days)
            # for opening_day in opening_days:
            #    temp_shop.opening_days.add(opening_day.pk)
            data = {
                'unique_id': unique_id,
                'shop_name': temp_shop.shop_name,
                'avatar': temp_shop.get_absolute_avatar_img,
                'color_code': temp_shop.color_code,
                'bg_color_code': temp_shop.bg_color_code,
                'font_name': temp_shop.font_name
            }
            # Generate thumbnail
            base_generate_avatar_thumbnail.apply_async((temp_shop.pk, 'TempShop'), )
            shift = datetime.utcnow() + timedelta(hours=24)
            task_id = base_start_deleting_expired_shops.apply_async((temp_shop.pk,), eta=shift)
            temp_shop.task_id = str(task_id)
            temp_shop.save()
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request, *args, **kwargs):
        unique_id = kwargs.get('unique_id')
        try:
            temp_shop = TempShop.objects.get(unique_id=unique_id)
            temp_shop_details_serializer = BaseGETTempShopInfoSerializer(temp_shop)
            return Response(temp_shop_details_serializer.data, status=status.HTTP_200_OK)
        except TempShop.DoesNotExist:
            data = {'errors': ['Temp shop not found.']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class TempShopAvatarPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopAvatarPutSerializer(data=request.data)
        if serializer.is_valid():
            if temp_shop.avatar:
                try:
                    remove(temp_shop.avatar.path)
                except (ValueError, SuspiciousFileOperation, FileNotFoundError):
                    pass
            if temp_shop.avatar_thumbnail:
                try:
                    remove(temp_shop.avatar_thumbnail.path)
                except (ValueError, SuspiciousFileOperation, FileNotFoundError):
                    pass
            new_avatar = serializer.update(temp_shop, serializer.validated_data)
            # Generate new avatar thumbnail
            base_generate_avatar_thumbnail.apply_async((new_avatar.pk,), )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopNamePutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopNamePutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(temp_shop, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopBioPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopBioPutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(temp_shop, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopAvailabilityPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopAvailabilityPutSerializer(data={
            'morning_hour_from': request.data.get('morning_hour_from'),
            'morning_hour_to': request.data.get('morning_hour_to'),
            'afternoon_hour_from': request.data.get('afternoon_hour_from'),
            'afternoon_hour_to': request.data.get('afternoon_hour_to'),
        })
        if serializer.is_valid():
            new_availability = serializer.update(temp_shop, serializer.validated_data)
            opening_days = str(request.data.get('opening_days')).split(',')
            opening_days = AuthShopDays.objects.filter(code_day__in=opening_days)
            new_availability.opening_days.clear()
            for day in opening_days:
                new_availability.opening_days.add(day.pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopContactPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopContactPutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(temp_shop, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopTelPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopTelPutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(temp_shop, serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopWtspPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopWtspPutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(temp_shop, serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopAddressPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopAddressPutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(temp_shop, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopColorPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopColorPutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(temp_shop, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempShopFontPutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        temp_shop = TempShop.objects.get(unique_id=unique_id)
        serializer = BaseTempShopFontPutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(temp_shop, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
