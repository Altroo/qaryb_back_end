# Generated by Django 4.1.2 on 2022-10-28 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0008_indexedarticles'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocodes',
            name='promo_code_for',
            field=models.CharField(choices=[('C', 'Create'), ('E', 'Edit')], default='C', max_length=1, verbose_name='Promo code for'),
        ),
    ]
