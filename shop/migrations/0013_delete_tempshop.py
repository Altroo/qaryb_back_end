# Generated by Django 4.1.2 on 2022-10-30 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0012_remove_tempoffers_auth_shop_and_more'),
        ('shop', '0012_alter_authshop_latitude_alter_authshop_longitude'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TempShop',
        ),
    ]
