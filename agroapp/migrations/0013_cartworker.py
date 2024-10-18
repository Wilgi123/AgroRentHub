# Generated by Django 5.0.6 on 2024-07-17 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroapp', '0012_alter_cartitem_end_date_alter_cartitem_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_workers', models.PositiveIntegerField()),
                ('work_type', models.CharField(max_length=100)),
                ('total_worker_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agroapp.farmer')),
            ],
        ),
    ]
