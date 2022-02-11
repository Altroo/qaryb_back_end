# Generated by Django 4.0.2 on 2022-02-09 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_shop', '0006_colors_sizes'),
    ]

    operations = [
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
    ]