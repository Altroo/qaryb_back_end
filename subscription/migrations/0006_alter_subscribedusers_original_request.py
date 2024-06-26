# Generated by Django 4.1 on 2022-10-21 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_alter_subscribedusers_facture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribedusers',
            name='original_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='original_request_subscribed_users', to='subscription.requestedsubscriptions', verbose_name='Original subscription'),
        ),
    ]
