# Generated by Django 4.0.2 on 2022-02-28 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_category', models.CharField(blank=True, default=None, max_length=2, null=True, unique=True)),
                ('name_category', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_color', models.CharField(blank=True, default=None, max_length=2, null=True, unique=True)),
                ('name_color', models.CharField(max_length=255, unique=True, verbose_name='Color Name')),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colors',
            },
        ),
        migrations.CreateModel(
            name='Days',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_day', models.CharField(blank=True, default=None, max_length=2, null=True, unique=True)),
                ('name_day', models.CharField(max_length=255, unique=True, verbose_name='Day name')),
            ],
            options={
                'verbose_name': 'Day',
                'verbose_name_plural': 'Days',
            },
        ),
        migrations.CreateModel(
            name='ForWhom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_for_whom', models.CharField(blank=True, default=None, max_length=2, null=True, unique=True)),
                ('name_for_whom', models.CharField(max_length=255, unique=True, verbose_name='For whom Name')),
            ],
            options={
                'verbose_name': 'For Whom',
                'verbose_name_plural': 'For Whom',
            },
        ),
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_size', models.CharField(blank=True, default=None, max_length=2, null=True, unique=True)),
                ('name_size', models.CharField(max_length=255, unique=True, verbose_name='Size Name')),
            ],
            options={
                'verbose_name': 'Size',
                'verbose_name_plural': 'Sizes',
            },
        ),
    ]
