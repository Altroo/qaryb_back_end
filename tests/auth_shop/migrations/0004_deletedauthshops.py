# Generated by Django 4.0.4 on 2022-05-19 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_shop', '0003_authshop_mode_vacance_task_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedAuthShops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_choice', models.CharField(blank=True, choices=[('', 'Unset'), ('A', 'Je cesse mon activité'), ('B', 'Je cesse mon activité 2')], default='', max_length=1, null=True)),
                ('typed_reason', models.CharField(blank=True, default='', max_length=140, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_auth_shops', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Deleted Store',
                'verbose_name_plural': 'Deleted Stores',
            },
        ),
    ]
