# Generated by Django 4.1.3 on 2022-12-06 10:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo_pages', '0003_alter_defaultseopage_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultseopage',
            name='indexed',
            field=models.BooleanField(default=False, verbose_name='Page indexed ?'),
        ),
        migrations.AlterField(
            model_name='defaultseopage',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Tags'), default=None, help_text='Separated by comma ","', size=None),
        ),
        migrations.AlterField(
            model_name='defaultseopage',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Title (h1)'),
        ),
    ]
