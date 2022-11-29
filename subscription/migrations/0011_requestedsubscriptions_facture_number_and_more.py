# Generated by Django 4.1.3 on 2022-11-28 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0010_remove_promocodes_promo_code_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestedsubscriptions',
            name='facture_number',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Facture number'),
        ),
        migrations.AlterField(
            model_name='promocodes',
            name='value',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='% price or nbr (depend on type)'),
        ),
        migrations.AlterField(
            model_name='requestedsubscriptions',
            name='reference_number',
            field=models.CharField(max_length=255, unique=True, verbose_name='Reference/Commande number'),
        ),
    ]
