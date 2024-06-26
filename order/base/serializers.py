from typing import Union
from django.db.models import QuerySet
from rest_framework import serializers
from order.models import OrderDetails, Order


class BaseOrderProductDetailsSerializerV2(serializers.Serializer):
    picked_quantity = serializers.IntegerField()
    picked_color = serializers.CharField()
    picked_size = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseOrderServiceDetailsSerializerV2(serializers.Serializer):
    picked_date = serializers.DateField()
    picked_hour = serializers.TimeField()
    service_zone_by = serializers.CharField()
    service_longitude = serializers.FloatField()
    service_latitude = serializers.FloatField()
    service_address = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseClickAndCollectSerializer(serializers.Serializer):
    product_longitude = serializers.FloatField()
    product_latitude = serializers.FloatField()
    product_address = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseDeliverySerializer(serializers.Serializer):
    delivery_price = serializers.FloatField()
    address = serializers.CharField()
    city = serializers.CharField()
    zip_code = serializers.IntegerField()
    country = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseOrderDetailsListSerializer(serializers.Serializer):
    offer_type = serializers.CharField()
    offer_title = serializers.CharField()
    offer_thumbnail = serializers.CharField(source='get_absolute_offer_thumbnail')
    offer_price = serializers.FloatField()
    offer_total_price = serializers.SerializerMethodField()
    offer_details = serializers.SerializerMethodField()
    picked_click_and_collect = serializers.BooleanField()
    click_and_collect = serializers.SerializerMethodField()
    picked_delivery = serializers.BooleanField()
    delivery = serializers.SerializerMethodField()

    @staticmethod
    def get_offer_total_price(instance):
        return instance.offer_price * instance.picked_quantity

    @staticmethod
    def get_delivery(instance):
        if instance.picked_delivery:
            serializer = BaseDeliverySerializer(instance)
            return serializer.data
        return {}

    @staticmethod
    def get_click_and_collect(instance):
        if instance.picked_click_and_collect:
            serializer = BaseClickAndCollectSerializer(instance)
            return serializer.data
        return {}

    @staticmethod
    def get_offer_details(instance):
        if instance.offer_type == 'V':
            details_product = BaseOrderProductDetailsSerializerV2(instance)
            return details_product.data
        if instance.offer_type == 'S':
            details_service = BaseOrderServiceDetailsSerializerV2(instance)
            return details_service.data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseOrdersListSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    link = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    order_number = serializers.CharField()
    order_date = serializers.DateTimeField()
    articles_count = serializers.SerializerMethodField()
    order_status = serializers.CharField()
    total_price = serializers.FloatField()
    order_details = BaseOrderDetailsListSerializer(many=True, source='order_details_order')
    note = serializers.CharField()
    highest_delivery_price = serializers.FloatField()
    order_for = serializers.SerializerMethodField()

    def get_link(self, instance):
        order_for = self.context.get("order_for")
        if order_for == 'S':
            if instance.buyer:
                return instance.buyer.pk
            else:
                return None
        else:
            return instance.seller.qaryb_link

    def get_first_name(self, instance):
        order_for = self.context.get("order_for")
        if order_for == 'S':
            return instance.first_name
        else:
            return instance.seller.shop_name

    def get_last_name(self, instance):
        order_for = self.context.get("order_for")
        if order_for == 'S':
            return instance.last_name
        else:
            return ''

    def get_avatar(self, instance):
        order_for = self.context.get("order_for")
        if order_for == 'S':
            return instance.get_absolute_buyer_thumbnail
        else:
            if instance.seller.get_absolute_avatar_thumbnail:
                return instance.seller.get_absolute_avatar_thumbnail
            else:
                return instance.seller.get_absolute_avatar_img

    def get_order_for(self, instance):
        return self.context.get("order_for")

    @staticmethod
    def get_articles_count(instance: Union[QuerySet, Order]):
        return OrderDetails.objects.filter(order=instance).count()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['seller', 'buyer', 'first_name', 'last_name',
                  'note', 'order_number', 'total_price']


class BaseOrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetails
        fields = ['order', 'offer', 'offer_type', 'offer_title', 'offer_price',
                  'picked_click_and_collect', 'product_longitude', 'product_latitude', 'product_address',
                  'picked_delivery', 'delivery_price', 'address', 'city', 'zip_code',
                  'country', 'phone', 'email', 'picked_color', 'picked_size', 'picked_quantity',
                  'picked_date', 'picked_hour', 'service_zone_by', 'service_longitude',
                  'service_latitude', 'service_address', 'service_km_radius']


class BaseChiffreAffaireListSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    order_number = serializers.CharField()
    order_date = serializers.DateTimeField()
    articles_count = serializers.SerializerMethodField()
    total_price = serializers.FloatField()

    @staticmethod
    def get_articles_count(instance: Union[QuerySet, Order]):
        return OrderDetails.objects.filter(order=instance).count()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
