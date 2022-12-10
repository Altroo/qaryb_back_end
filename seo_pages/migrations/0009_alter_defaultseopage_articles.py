# Generated by Django 4.1.4 on 2022-12-08 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0016_indexedarticles_status'),
        ('seo_pages', '0008_defaultseopage_articles_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultseopage',
            name='articles',
            field=models.ManyToManyField(blank=True, related_name='default_seo_page_indexed_articles', to='subscription.indexedarticles', verbose_name='Articles'),
        ),
    ]
