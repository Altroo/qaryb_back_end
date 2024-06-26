# Generated by Django 4.1.4 on 2022-12-16 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_orderdetails_service_km_radius_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_delivery_price',
            new_name='highest_delivery_price',
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(blank=True, default=0, help_text='all offers price (solder & quantity). deliveries excluded', null=True, verbose_name='Order total price'),
        ),
    ]
