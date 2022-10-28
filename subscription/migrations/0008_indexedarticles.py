# Generated by Django 4.1 on 2022-10-24 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0011_alter_offers_creator_label_and_more'),
        ('subscription', '0007_alter_requestedsubscriptions_payment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexedArticles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_offer', to='offers.offers', verbose_name='Offer')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_indexed_articles', to='subscription.subscribedusers', verbose_name='Subscription')),
            ],
            options={
                'verbose_name': 'Indexed article',
                'verbose_name_plural': 'Indexed articles',
                'ordering': ('-pk',),
            },
        ),
    ]