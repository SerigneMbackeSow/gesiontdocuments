# Generated by Django 3.1.13 on 2024-05-27 02:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturations', '0006_mig17'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='eta',
            field=models.DateField(default=datetime.datetime(2024, 5, 27, 4, 43, 32, 429219)),
        ),
    ]
