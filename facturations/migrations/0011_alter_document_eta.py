# Generated by Django 5.0.6 on 2024-08-12 18:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturations', '0010_alter_document_eta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='eta',
            field=models.DateField(default=datetime.datetime(2024, 8, 12, 20, 54, 1, 490285)),
        ),
    ]
