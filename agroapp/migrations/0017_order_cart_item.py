# Generated by Django 5.0.6 on 2024-07-31 09:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroapp', '0016_order_delete_cartworker'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='agroapp.cartitem'),
        ),
    ]
