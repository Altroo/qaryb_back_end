# Generated by Django 4.1 on 2022-10-07 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
        ('offers', '0010_alter_offers_made_in_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='creator_label',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Creator label'),
        ),
        migrations.AlterField(
            model_name='offers',
            name='made_in_label',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'country'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_offer', to='places.country', verbose_name='Made in'),
        ),
        migrations.AlterField(
            model_name='tempoffers',
            name='made_in_label',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'country'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_temp_offer', to='places.country', verbose_name='Made in'),
        ),
    ]
