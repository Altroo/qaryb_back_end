# Generated by Django 4.1.4 on 2022-12-16 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_remove_orderdetails_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetails',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='service_km_radius',
        ),
    ]
