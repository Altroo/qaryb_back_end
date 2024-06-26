from rest_framework import serializers
from shop.models import AuthShop, AskForCreatorLabel, ModeVacance, AuthShopDays
from shop.base.utils import Base64ImageField
from subscription.models import SubscribedUsers
from django.utils import timezone


class BaseShopSerializer(serializers.ModelSerializer):
    # avatar = Base64ImageField(
    #     max_length=None, use_url=True,
    # )

    class Meta:
        model = AuthShop
        fields = [
            'user',
            'shop_name',
            'color_code', 'bg_color_code', 'border', 'icon_color',
            'font_name',
            'creator']

    def save(self):
        shop = AuthShop(
            user=self.validated_data['user'],
            shop_name=self.validated_data['shop_name'],
            color_code=self.validated_data['color_code'],
            bg_color_code=self.validated_data['bg_color_code'],
            border=self.validated_data['border'],
            icon_color=self.validated_data['icon_color'],
            font_name=self.validated_data['font_name'],
            # Read only default to False
            creator=self.validated_data['creator'],
        )
        shop.save()
        return shop


class BaseProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthShopDays
        fields = ['pk', 'code_day', 'name_day']


class BaseGETShopInfoSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='get_absolute_avatar_img')
    avatar_thumbnail = serializers.CharField(source='get_absolute_avatar_thumbnail')
    # opening_days = serializers.SerializerMethodField()
    opening_days = BaseProductColorSerializer(many=True, read_only=True)
    morning_hour_from = serializers.TimeField(format='%H:%M')
    morning_hour_to = serializers.TimeField(format='%H:%M')
    afternoon_hour_from = serializers.TimeField(format='%H:%M')
    afternoon_hour_to = serializers.TimeField(format='%H:%M')
    is_subscribed = serializers.SerializerMethodField()

    @staticmethod
    def get_is_subscribed(instance):
        try:
            # TODO fix duplicate
            subscription = SubscribedUsers.objects.get(original_request__auth_shop=instance.pk)
            present = timezone.now()
            if present < subscription.expiration_date:
                return True
            return False
        except SubscribedUsers.DoesNotExist:
            return False

    # @staticmethod
    # def get_opening_days(instance):
    #     return instance.opening_days.values_list('code_day', flat=True)

    class Meta:
        model = AuthShop
        # has pk & creator
        fields = ['pk', 'user', 'shop_name', 'avatar', 'avatar_thumbnail', 'color_code', 'bg_color_code',
                  'border', 'icon_color',
                  'font_name', 'bio',
                  'opening_days', 'morning_hour_from', 'morning_hour_to',
                  'afternoon_hour_from', 'afternoon_hour_to',
                  'contact_phone_code', 'contact_phone', 'contact_whatsapp_code', 'contact_whatsapp', 'contact_mode',
                  'phone', 'contact_email',
                  'website_link', 'facebook_link', 'twitter_link', 'instagram_link',
                  'whatsapp', 'zone_by', 'longitude', 'latitude',
                  'address_name', 'km_radius', 'creator', 'is_subscribed']


class BaseShopAvatarPutSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = AuthShop
        fields = ['avatar']
        extra_kwargs = {
            'avatar': {'required': True},
        }

    # def update(self, instance, validated_data):
    #     instance.avatar = validated_data.get('avatar', instance.avatar)
    #     instance.save()
    #     return instance


class BaseShopNamePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthShop
        fields = ['shop_name']
        extra_kwargs = {
            'shop_name': {'required': True},
        }

    # def update(self, instance, validated_data):
    #     instance.shop_name = validated_data.get('shop_name', instance.shop_name)
    #     instance.save()
    #     return instance


class BaseShopBioPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthShop
        fields = ['bio']
        extra_kwargs = {
            'bio': {'required': True},
        }

    # def update(self, instance, validated_data):
    #     instance.bio = validated_data.get('bio', instance.bio)
    #     instance.save()
    #     return instance


class BaseShopAvailabilityPutSerializer(serializers.ModelSerializer):
    morning_hour_from = serializers.TimeField(format='%H:%M', required=False, allow_null=True, default=None)
    morning_hour_to = serializers.TimeField(format='%H:%M', required=False, allow_null=True, default=None)
    afternoon_hour_from = serializers.TimeField(format='%H:%M', required=False, allow_null=True, default=None)
    afternoon_hour_to = serializers.TimeField(format='%H:%M', required=False, allow_null=True, default=None)

    class Meta:
        model = AuthShop
        fields = ['morning_hour_from', 'morning_hour_to',
                  'afternoon_hour_from', 'afternoon_hour_to']

    # def update(self, instance, validated_data):
    #     instance.morning_hour_from = validated_data.get('morning_hour_from', instance.morning_hour_from)
    #     instance.morning_hour_to = validated_data.get('morning_hour_to', instance.morning_hour_to)
    #     instance.afternoon_hour_from = validated_data.get('afternoon_hour_from', instance.afternoon_hour_from)
    #     instance.afternoon_hour_to = validated_data.get('afternoon_hour_to', instance.afternoon_hour_to)
    #     instance.save()
    #     return instance


class BaseShopContactPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthShop
        fields = ['phone', 'contact_email',
                  'website_link',
                  'facebook_link', 'twitter_link', 'instagram_link', 'whatsapp']

    # def update(self, instance, validated_data):
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.contact_email = validated_data.get('contact_email', instance.contact_email)
    #     instance.website_link = validated_data.get('website_link', instance.website_link)
    #     instance.facebook_link = validated_data.get('facebook_link', instance.facebook_link)
    #     instance.twitter_link = validated_data.get('twitter_link', instance.twitter_link)
    #     instance.instagram_link = validated_data.get('instagram_link', instance.instagram_link)
    #     instance.whatsapp = validated_data.get('whatsapp', instance.whatsapp)
    #     instance.save()
    #     return instance


class BaseShopPhoneContactPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthShop
        fields = ['contact_phone_code', 'contact_phone', 'contact_whatsapp_code', 'contact_whatsapp', 'contact_mode']

    # def update(self, instance, validated_data):
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.save()
    #     return instance


# class BaseShopWtspPutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AuthShop
#         fields = ['whatsapp_code', 'whatsapp']

    # def update(self, instance, validated_data):
    #     instance.whatsapp = validated_data.get('whatsapp', instance.whatsapp)
    #     instance.save()
    #     return instance


class BaseShopAddressPutSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that start is before finish.
        """
        data_keys = data.keys()
        if data['zone_by'] == 'S' and 'km_radius' not in data_keys:
            raise serializers.ValidationError({'km_radius': ['km_radius is required when zone is by Sector.']})
        return data

    class Meta:
        model = AuthShop
        fields = ['zone_by', 'longitude', 'latitude', 'address_name', 'km_radius']
        extra_kwargs = {
            'zone_by': {'required': True},
            'longitude': {'required': True},
            'latitude': {'required': True},
            'address_name': {'required': True},
        }

    # def update(self, instance, validated_data):
    #     instance.zone_by = validated_data.get('zone_by', instance.zone_by)
    #     instance.longitude = validated_data.get('longitude', instance.longitude)
    #     instance.latitude = validated_data.get('latitude', instance.latitude)
    #     instance.address_name = validated_data.get('address_name', instance.address_name)
    #     instance.km_radius = validated_data.get('km_radius', instance.km_radius)
    #     instance.save()
    #     return instance


class BaseShopColorPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthShop
        fields = ['color_code', 'bg_color_code', 'border', 'icon_color']
        extra_kwargs = {
            'color_code': {'required': True},
            'bg_color_code': {'required': True},
            'border': {'required': True},
            'icon_color': {'required': True},
        }

    # def update(self, instance, validated_data):
    #     instance.color_code = validated_data.get('color_code', instance.color_code)
    #     instance.bg_color_code = validated_data.get('bg_color_code', instance.bg_color_code)
    #     instance.save()
    #     return instance


class BaseShopFontPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthShop
        fields = ['font_name']
        extra_kwargs = {
            'font_name': {'required': True},
        }

    # def update(self, instance, validated_data):
    #     instance.font_name = validated_data.get('font_name', instance.font_name)
    #     instance.save()
    #     return instance


class BaseShopAskForCreatorLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AskForCreatorLabel
        fields = ['auth_shop']


class BaseShopModeVacanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeVacance
        fields = ['auth_shop', 'date_from', 'date_to']


class BaseShopModeVacancePUTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeVacance
        fields = ['date_from', 'date_to']

    # def update(self, instance, validated_data):
    #     instance.date_from = validated_data.get('date_from', instance.date_from)
    #     instance.date_to = validated_data.get('date_to', instance.date_to)
    #     instance.save()
    #     return instance


# class BaseTempShopSerializer(serializers.ModelSerializer):
#     avatar = Base64ImageField(
#         max_length=None, use_url=True,
#     )
#
#     class Meta:
#         model = TempShop
#         fields = ['shop_name',
#                   'avatar', 'color_code', 'bg_color_code', 'border', 'icon_color',
#                   'font_name',
#                   'unique_id']
#         extra_kwargs = {
#             'avatar': {'required': True},
#         }
#
#     def save(self):
#         shop = TempShop(
#             shop_name=self.validated_data['shop_name'],
#             avatar=self.validated_data['avatar'],
#             color_code=self.validated_data['color_code'],
#             bg_color_code=self.validated_data['bg_color_code'],
#             border=self.validated_data['border'],
#             icon_color=self.validated_data['icon_color'],
#             font_name=self.validated_data['font_name'],
#             unique_id=self.validated_data['unique_id'],
#         )
#         shop.save()
#         return shop
#
#
# class BaseGETTempShopInfoSerializer(serializers.ModelSerializer):
#     avatar = serializers.CharField(source='get_absolute_avatar_img')
#     avatar_thumbnail = serializers.CharField(source='get_absolute_avatar_thumbnail')
#     # opening_days = serializers.SerializerMethodField()
#     opening_days = BaseProductColorSerializer(many=True, read_only=True)
#     morning_hour_from = serializers.TimeField(format='%H:%M')
#     morning_hour_to = serializers.TimeField(format='%H:%M')
#     afternoon_hour_from = serializers.TimeField(format='%H:%M')
#     afternoon_hour_to = serializers.TimeField(format='%H:%M')
#
#     # @staticmethod
#     # def get_opening_days(instance):
#     #     return instance.opening_days.values_list('code_day', flat=True)
#
#     class Meta:
#         model = TempShop
#         # has not pk & creator
#         fields = ['shop_name', 'avatar', 'avatar_thumbnail',
#                   'color_code', 'bg_color_code',
#                   'border', 'icon_color',
#                   'font_name', 'bio',
#                   'opening_days', 'morning_hour_from', 'morning_hour_to',
#                   'afternoon_hour_from', 'afternoon_hour_to',
#                   'contact_phone_code', 'contact_phone', 'contact_whatsapp_code', 'contact_whatsapp', 'contact_mode',
#                   'phone', 'contact_email',
#                   'website_link', 'facebook_link', 'twitter_link', 'instagram_link',
#                   'whatsapp', 'zone_by', 'longitude', 'latitude',
#                   'address_name', 'km_radius']
#
#
# class BaseTempShopAvatarPutSerializer(serializers.ModelSerializer):
#     avatar = Base64ImageField(
#         max_length=None, use_url=True,
#     )
#
#     class Meta:
#         model = TempShop
#         fields = ['avatar']
#         extra_kwargs = {
#             'avatar': {'required': True},
#         }
#
#     # def update(self, instance, validated_data):
#     #     instance.avatar = validated_data.get('avatar', instance.avatar)
#     #     instance.save()
#     #     return instance
#
#
# class BaseTempShopNamePutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempShop
#         fields = ['shop_name']
#         extra_kwargs = {
#             'shop_name': {'required': True},
#         }
#
#     # def update(self, instance, validated_data):
#     #    instance.shop_name = validated_data.get('shop_name', instance.shop_name)
#     #    instance.save()
#     #    return instance
#
#
# class BaseTempShopBioPutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempShop
#         fields = ['bio']
#         extra_kwargs = {
#             'bio': {'required': True},
#         }
#
#     # def update(self, instance, validated_data):
#     #     instance.bio = validated_data.get('bio', instance.bio)
#     #     instance.save()
#     #     return instance
#
#
# class BaseTempShopAvailabilityPutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempShop
#         fields = ['morning_hour_from', 'morning_hour_to',
#                   'afternoon_hour_from', 'afternoon_hour_to']
#
#     # def update(self, instance, validated_data):
#     #     instance.morning_hour_from = validated_data.get('morning_hour_from', instance.morning_hour_from)
#     #     instance.morning_hour_to = validated_data.get('morning_hour_to', instance.morning_hour_to)
#     #     instance.afternoon_hour_from = validated_data.get('afternoon_hour_from', instance.afternoon_hour_from)
#     #     instance.afternoon_hour_to = validated_data.get('afternoon_hour_to', instance.afternoon_hour_to)
#     #     instance.save()
#     #     return instance
#
#
# class BaseTempShopContactPutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempShop
#         fields = ['phone', 'contact_email',
#                   'website_link',
#                   'facebook_link', 'twitter_link', 'instagram_link', 'whatsapp']
#
#     # def update(self, instance, validated_data):
#     #     instance.phone = validated_data.get('phone', instance.phone)
#     #     instance.contact_email = validated_data.get('contact_email', instance.contact_email)
#     #     instance.website_link = validated_data.get('website_link', instance.website_link)
#     #     instance.facebook_link = validated_data.get('facebook_link', instance.facebook_link)
#     #     instance.twitter_link = validated_data.get('twitter_link', instance.twitter_link)
#     #     instance.instagram_link = validated_data.get('instagram_link', instance.instagram_link)
#     #     instance.whatsapp = validated_data.get('whatsapp', instance.whatsapp)
#     #     instance.save()
#     #     return instance
#
#
# class BaseTempShopPhoneContactPutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempShop
#         fields = ['contact_phone_code', 'contact_phone', 'contact_whatsapp_code', 'contact_whatsapp', 'contact_mode']
#
#     # def update(self, instance, validated_data):
#     #     instance.phone = validated_data.get('phone', instance.phone)
#     #     instance.save()
#     #     return instance


# class BaseTempShopWtspPutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempShop
#         fields = ['whatsapp_code', 'whatsapp']
#
#     # def update(self, instance, validated_data):
#     #     instance.whatsapp = validated_data.get('whatsapp', instance.whatsapp)
#     #     instance.save()
#     #     return instance

#
# class BaseTempShopAddressPutSerializer(serializers.ModelSerializer):
#     def validate(self, data):
#         """
#         Check that start is before finish.
#         """
#         data_keys = data.keys()
#         if data['zone_by'] == 'S' and 'km_radius' not in data_keys:
#             raise serializers.ValidationError({'km_radius': ['km_radius is required when zone is by Sector.']})
#         return data
#
#     class Meta:
#         model = TempShop
#         fields = ['zone_by', 'longitude', 'latitude', 'address_name', 'km_radius']
#         extra_kwargs = {
#             'zone_by': {'required': True},
#             'longitude': {'required': True},
#             'latitude': {'required': True},
#             'address_name': {'required': True},
#         }
#
#     # def update(self, instance, validated_data):
#     #     instance.zone_by = validated_data.get('zone_by', instance.zone_by)
#     #     instance.longitude = validated_data.get('longitude', instance.longitude)
#     #     instance.latitude = validated_data.get('latitude', instance.latitude)
#     #     instance.address_name = validated_data.get('address_name', instance.address_name)
#     #     instance.km_radius = validated_data.get('km_radius', instance.km_radius)
#     #     instance.save()
#     #     return instance
#
#
# class BaseTempShopColorPutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempShop
#         fields = ['color_code', 'bg_color_code', 'border', 'icon_color']
#         extra_kwargs = {
#             'color_code': {'required': True},
#             'bg_color_code': {'required': True},
#             'border': {'required': True},
#             'icon_color': {'required': True},
#         }
#
#     # def update(self, instance, validated_data):
#     #     instance.color_code = validated_data.get('color_code', instance.color_code)
#     #     instance.bg_color_code = validated_data.get('bg_color_code', instance.bg_color_code)
#     #     instance.save()
#     #     return instance
#
#
# class BaseTempShopFontPutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempShop
#         fields = ['font_name']
#         extra_kwargs = {
#             'font_name': {'required': True},
#         }
#
#     # def update(self, instance, validated_data):
#     #     instance.font_name = validated_data.get('font_name', instance.font_name)
#     #     instance.save()
#     #     return instance
