# Generated by Django 4.0.4 on 2022-05-09 08:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import offer.base.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('offer', '0001_initial'),
        ('temp_shop', '0001_initial'),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempOffers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_type', models.CharField(choices=[('V', 'Sell'), ('S', 'Service'), ('L', 'Location')], max_length=1, verbose_name='Offer Type')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('picture_1', models.ImageField(blank=True, default=None, max_length=1000, null=True, upload_to=offer.base.models.get_shop_offers_path, verbose_name='Picture 1')),
                ('picture_2', models.ImageField(blank=True, default=None, max_length=1000, null=True, upload_to=offer.base.models.get_shop_offers_path, verbose_name='Picture 2')),
                ('picture_3', models.ImageField(blank=True, default=None, max_length=1000, null=True, upload_to=offer.base.models.get_shop_offers_path, verbose_name='Picture 3')),
                ('picture_1_thumbnail', models.ImageField(blank=True, max_length=1000, null=True, upload_to=offer.base.models.get_shop_offers_path, verbose_name='Picture 1 thumbnail')),
                ('picture_2_thumbnail', models.ImageField(blank=True, max_length=1000, null=True, upload_to=offer.base.models.get_shop_offers_path, verbose_name='Picture 2 thumbnail')),
                ('picture_3_thumbnail', models.ImageField(blank=True, max_length=1000, null=True, upload_to=offer.base.models.get_shop_offers_path, verbose_name='Picture 3 thumbnail')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('price', models.FloatField(default=0.0, verbose_name='Price')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('for_whom', models.ManyToManyField(related_name='temp_offer_for_whom', to='offer.forwhom', verbose_name='For Whom')),
                ('offer_categories', models.ManyToManyField(related_name='temp_offer_categories', to='offer.categories', verbose_name='Offer Categories')),
                ('tags', models.ManyToManyField(related_name='temp_offer_tags', to='offer.offertags', verbose_name='Temp Offer Tags')),
                ('temp_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temp_shop', to='temp_shop.tempshop', verbose_name='Temp Shop')),
            ],
            options={
                'verbose_name': 'Temp Offer',
                'verbose_name_plural': 'Temp Offers',
                'ordering': ('created_date',),
            },
        ),
        migrations.CreateModel(
            name='TempSolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_solder_type', models.CharField(choices=[('F', 'Prix fix'), ('P', 'Pourcentage')], max_length=1, verbose_name='Temp solder type')),
                ('temp_solder_value', models.FloatField(default=0.0, verbose_name='Temp solder value')),
                ('temp_offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temp_offer_solder', to='temp_offer.tempoffers', verbose_name='Temp Offer')),
            ],
            options={
                'verbose_name': 'Temp Solder',
                'verbose_name_plural': 'Temp Solders',
            },
        ),
        migrations.CreateModel(
            name='TempServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_morning_hour_from', models.TimeField(blank=True, default=None, null=True, verbose_name='Morning hour from')),
                ('service_morning_hour_to', models.TimeField(blank=True, default=None, null=True, verbose_name='Morning hour to')),
                ('service_afternoon_hour_from', models.TimeField(blank=True, default=None, null=True, verbose_name='Afternoon hour from')),
                ('service_afternoon_hour_to', models.TimeField(blank=True, default=None, null=True, verbose_name='Afternoon hour to')),
                ('service_zone_by', models.CharField(choices=[('A', 'Address'), ('S', 'Sector')], default='A', max_length=1, verbose_name='Zone by')),
                ('service_price_by', models.CharField(choices=[('H', 'Heur'), ('J', 'Jour'), ('S', 'Semaine'), ('M', 'Mois'), ('P', 'Prestation')], max_length=1, verbose_name='Price by')),
                ('service_longitude', models.FloatField(blank=True, default=None, max_length=10, null=True, validators=[django.core.validators.RegexValidator('^(\\+|-)?(?:180(?:(?:\\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\\.[0-9]{1,6})?))$', 'Only Geo numbers are allowed.')], verbose_name='Service Longitude')),
                ('service_latitude', models.FloatField(blank=True, default=None, max_length=10, null=True, validators=[django.core.validators.RegexValidator('^(\\+|-)?(?:90(?:(?:\\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\\.[0-9]{1,6})?))$', 'Only Geo numbers are allowed.')], verbose_name='Service Latitude')),
                ('service_address', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Service Address')),
                ('service_km_radius', models.FloatField(blank=True, default=None, null=True, verbose_name='Km radius')),
                ('service_availability_days', models.ManyToManyField(related_name='temp_service_availability_days', to='offer.servicedays', verbose_name='Opening days')),
                ('temp_offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temp_offer_services', to='temp_offer.tempoffers', verbose_name='Temp Offer')),
            ],
            options={
                'verbose_name': 'Temp Service',
                'verbose_name_plural': 'Temp Services',
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='TempProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='Quantity')),
                ('product_price_by', models.CharField(choices=[('U', 'Unity'), ('K', 'Kilogram'), ('L', 'Liter')], max_length=1, verbose_name='Price by')),
                ('product_longitude', models.FloatField(blank=True, default=None, max_length=10, null=True, validators=[django.core.validators.RegexValidator('^(\\+|-)?(?:180(?:(?:\\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\\.[0-9]{1,6})?))$', 'Only Geo numbers are allowed.')], verbose_name='Product Longitude')),
                ('product_latitude', models.FloatField(blank=True, default=None, max_length=10, null=True, validators=[django.core.validators.RegexValidator('^(\\+|-)?(?:90(?:(?:\\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\\.[0-9]{1,6})?))$', 'Only Geo numbers are allowed.')], verbose_name='Product Latitude')),
                ('product_address', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Product Address')),
                ('product_colors', models.ManyToManyField(related_name='temp_product_colors', to='offer.colors', verbose_name='Product Colors')),
                ('product_sizes', models.ManyToManyField(related_name='temp_product_sizes', to='offer.sizes', verbose_name='Product Sizes')),
                ('temp_offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temp_offer_products', to='temp_offer.tempoffers', verbose_name='Temp Offer')),
            ],
            options={
                'verbose_name': 'Temp Product',
                'verbose_name_plural': 'Temp Products',
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='TempDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_delivery_price', models.FloatField(default=0.0, verbose_name='Temp delivery Price')),
                ('temp_delivery_days', models.PositiveIntegerField(default=0, verbose_name='Temp number of Days')),
                ('temp_delivery_city', models.ManyToManyField(related_name='temp_delivery_city', to='places.city', verbose_name='Temp Delivery City')),
                ('temp_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temp_offer_delivery', to='temp_offer.tempoffers', verbose_name='Temp Offer')),
            ],
            options={
                'verbose_name': 'Temp Delivery',
                'verbose_name_plural': 'Temp Deliveries',
            },
        ),
    ]
