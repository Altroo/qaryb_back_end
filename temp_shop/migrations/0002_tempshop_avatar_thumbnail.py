# Generated by Django 4.0.2 on 2022-02-22 10:44

import auth_shop.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempshop',
            name='avatar_thumbnail',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=auth_shop.models.get_avatar_path, verbose_name='Avatar'),
        ),
    ]