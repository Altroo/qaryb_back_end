# Generated by Django 4.1 on 2022-10-21 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_alter_promocodes_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribedusers',
            name='facture',
            field=models.FilePathField(blank=True, default=None, null=True, path='media/files/', verbose_name='Facture'),
        ),
    ]
