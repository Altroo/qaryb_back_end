# Generated by Django 4.0.6 on 2022-07-14 17:53

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempshop',
            name='avatar_thumbnail',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=shop.models.get_shop_avatar_path, verbose_name='Avatar thumbnail'),
        ),
    ]