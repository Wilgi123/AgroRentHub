# Generated by Django 5.0.6 on 2024-07-31 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agroapp', '0018_alter_order_cart_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_item',
        ),
    ]
