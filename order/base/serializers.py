from rest_framework import serializers
from offer.base.models import Solder
from order.base.models import OrderDetails


class BaseDetailsOrderProductSerializer(serializers.Serializer):
    title = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseDetailsOrderServiceSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    # TODO check if price might include x quantity
    @staticmethod
    def get_price(instance):
        try:
            solder = Solder.objects.get(offer=instance.offer.pk)
            # Réduction fix
            if solder.solder_type == 'F':
                offer_price = instance.offer.price - solder.solder_value
            # Réduction Pourcentage
            else:
                offer_price = instance.offer.price - (instance.offer.price * solder.solder_value / 100)
            return offer_price * instance.picked_quantity
        except Solder.DoesNotExist:
            return instance.offer.price * instance.picked_quantity

    @staticmethod
    def get_thumbnail(instance):
        return instance.get_absolute_offer_thumbnail

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


# For naming convention
# TODO include services
class BaseTempOrdersListSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    avatar = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    title = serializers.CharField()
    total_price = serializers.SerializerMethodField()
    order_status = serializers.CharField()
    order_date = serializers.DateTimeField()
    viewed_buyer = serializers.BooleanField()

    def get_avatar(self, instance):
        if self.context.get('order_type') == 'buy':
            return instance.buyer.get_absolute_avatar_thumbnail
        return instance.seller.get_absolute_avatar_thumbnail

    def get_name(self, instance):
        if self.context.get('order_type') == 'buy':
            return instance.buyer.first_name + ' ' + instance.buyer.last_name
        return instance.seller.shop_name

    @staticmethod
    def get_total_price(instance):
        order_detail = OrderDetails.objects.filter(order=instance.pk)
        if len(order_detail) == 1:
            return order_detail[0].total_self_price
        price = 0
        for i in order_detail:
            price += i.total_self_price
        return price

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseOrderDetailsTypeListSerializer(serializers.Serializer):
    # Can include multiple products / multiple services / mixed products + services
    order_details = serializers.SerializerMethodField()

    @staticmethod
    def get_order_details(instance):
        # order product details
        if instance.offer_type == 'V':
            details_product = BaseDetailsOrderProductSerializer(instance)
            return details_product.data
        # order service details
        if instance.offer_type == 'S':
            details_service = BaseDetailsOrderServiceSerializer(instance)
            return details_service.data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


# Include mixed multiple orders (Products + Services)
class BaseOrderDetailsListSerializer(serializers.Serializer):
    # From Order model :
    # Buer name or seller shop name (check order type)
    order_initiator_name = serializers.SerializerMethodField()
    order_number = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()
    # From Order details model :
    order_details = BaseOrderDetailsTypeListSerializer(many=True)
    # Order details ID
    # Title
    # If product show :
    # Offer thumbnail 1
    # Price by quantity - solder ?
    # Picked color
    # Picked size
    # Picked quantity
    # If service show :
    # picked date
    # picked hour
    # Note
    # Check picked_click and collect if true show only :
    # Show product longitude
    # Show product_latitude
    # Show product_address
    # If service show :
    # Price - solder ?
    # service by sector, address
    # if sector add km range
    # else add service longitude + service latitde + service_address
    # else show buyer coordinates:
    # Fist_name
    # Last_name
    # address
    # city
    # zip_code
    # country
    # phone
    # Total needs to be calculated separately

    def get_order_initiator_name(self, instance):
        if self.context.get("order_type") == "buy":
            return instance.order.seller.shop_name
        return instance.order.buyer.first_name + ' ' + instance.order.buyer.last_name

    @staticmethod
    def get_order_number(instance):
        return instance.order.order_number

    @staticmethod
    def get_order_date(instance):
        return instance.order.order_date

    @staticmethod
    def get_order_status(instance):
        return instance.order.order_status

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

