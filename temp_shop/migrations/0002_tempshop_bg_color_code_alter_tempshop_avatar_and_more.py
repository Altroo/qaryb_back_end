# Generated by Django 4.0.3 on 2022-03-07 09:20

import auth_shop.models
import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempshop',
            name='bg_color_code',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, verbose_name='Color code'),
        ),
        migrations.AlterField(
            model_name='tempshop',
            name='avatar',
            field=models.ImageField(default=None, upload_to=auth_shop.models.get_avatar_path, verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='tempshop',
            name='color_code',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, verbose_name='Color code'),
        ),
        migrations.AlterField(
            model_name='tempshop',
            name='font_name',
            field=models.CharField(choices=[('LI', 'Light'), ('BO', 'Boldy'), ('CL', 'Classic'), ('MA', 'Magazine'), ('PO', 'Pop'), ('SA', 'Sans'), ('PA', 'Pacifico'), ('FI', 'Fira')], default='L', max_length=2, verbose_name='Font name'),
        ),
    ]
