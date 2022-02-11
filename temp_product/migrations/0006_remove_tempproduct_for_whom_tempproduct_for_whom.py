# Generated by Django 4.0.2 on 2022-02-09 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_shop', '0007_forwhom'),
        ('temp_product', '0005_remove_tempdelivery_temp_delivery_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempproduct',
            name='for_whom',
        ),
        migrations.AddField(
            model_name='tempproduct',
            name='for_whom',
            field=models.ManyToManyField(related_name='temp_product_for_whom', to='auth_shop.ForWhom', verbose_name='For Whom'),
        ),
    ]
