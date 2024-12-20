# Generated by Django 5.0.6 on 2024-08-22 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroapp', '0032_productdamage'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnrequest',
            name='total_repair_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
