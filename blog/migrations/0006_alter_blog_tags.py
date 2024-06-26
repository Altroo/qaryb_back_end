# Generated by Django 4.1.5 on 2023-01-12 21:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_background_image_alt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Tags'), blank=True, default=None, help_text='Separated by comma ","', null=True, size=None),
        ),
    ]
