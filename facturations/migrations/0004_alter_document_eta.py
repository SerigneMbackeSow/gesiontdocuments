# Generated by Django 5.0.6 on 2024-07-29 13:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturations', '0003_alter_document_eta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='eta',
            field=models.DateField(default=datetime.datetime(2024, 7, 29, 15, 0, 1, 430557)),
        ),
    ]
