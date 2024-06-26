# Generated by Django 4.1.3 on 2022-11-14 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_delete_tempshop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authshop',
            name='facebook_link',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='authshop',
            name='instagram_link',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Instagram'),
        ),
        migrations.AlterField(
            model_name='authshop',
            name='twitter_link',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Twitter'),
        ),
        migrations.AlterField(
            model_name='authshop',
            name='website_link',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Website'),
        ),
    ]
