# Generated by Django 4.0.4 on 2022-05-09 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0003_remove_offervue_date_offervue_nbr_total_vue_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offerstotalvues',
            old_name='offer_vue',
            new_name='offer',
        ),
        migrations.AlterUniqueTogether(
            name='offerstotalvues',
            unique_together={('offer', 'date')},
        ),
    ]
