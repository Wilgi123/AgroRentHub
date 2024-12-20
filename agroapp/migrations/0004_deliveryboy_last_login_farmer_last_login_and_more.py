# Generated by Django 5.0.6 on 2024-06-19 11:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroapp', '0003_remove_deliveryboy_last_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboy',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='farmer',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='supplier',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
