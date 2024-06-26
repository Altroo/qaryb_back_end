# Generated by Django 4.1.5 on 2023-01-05 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0017_indexedarticles_email_informed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indexedarticles',
            options={'ordering': ('-updated_date', '-created_date'), 'verbose_name': 'Article (référencer)', 'verbose_name_plural': 'Articles (référencer)'},
        ),
        migrations.AlterField(
            model_name='indexedarticles',
            name='status',
            field=models.CharField(choices=[('P', 'Non seo'), ('I', 'Seo'), ('U', 'Mis à jour')], default='P', max_length=1, verbose_name='Status'),
        ),
    ]
