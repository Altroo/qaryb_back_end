# Generated by Django 4.1 on 2022-09-08 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_offers_picture_4_offers_picture_4_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='pinned',
            field=models.BooleanField(default=False, verbose_name='Pinned ?'),
        ),
        migrations.AddField(
            model_name='tempoffers',
            name='pinned',
            field=models.BooleanField(default=False, verbose_name='Pinned ?'),
        ),
    ]
