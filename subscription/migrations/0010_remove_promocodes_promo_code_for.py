# Generated by Django 4.1.2 on 2022-10-30 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0009_promocodes_promo_code_for'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promocodes',
            name='promo_code_for',
        ),
    ]
