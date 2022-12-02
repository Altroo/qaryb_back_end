# Generated by Django 4.1 on 2022-10-07 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
        ('offers', '0009_tempoffers_made_in_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='made_in_label',
            field=models.ForeignKey(blank=True, default=None, limit_choices_to={'type': 'country'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_offer', to='places.country', verbose_name='Made in'),
        ),
        migrations.AlterField(
            model_name='tempoffers',
            name='made_in_label',
            field=models.ForeignKey(blank=True, default=None, limit_choices_to={'type': 'country'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_temp_offer', to='places.country', verbose_name='Made in'),
        ),
    ]