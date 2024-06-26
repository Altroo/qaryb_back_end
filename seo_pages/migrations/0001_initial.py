# Generated by Django 4.1.3 on 2022-12-05 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultSeoPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_url', models.SlugField(blank=True, default=None, max_length=255, null=True, unique=True, verbose_name='Page url (unique)')),
                ('title', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Title')),
                ('header', models.TextField(blank=True, default=None, null=True, verbose_name='Bold Header')),
                ('paragraphe', models.TextField(blank=True, default=None, null=True, verbose_name='Paragraphe')),
                ('page_meta_description', models.TextField(blank=True, default=None, null=True, verbose_name='Meta description')),
            ],
            options={
                'verbose_name': 'Default seo page',
                'verbose_name_plural': 'Default seo pages',
                'ordering': ('-pk',),
            },
        ),
    ]
