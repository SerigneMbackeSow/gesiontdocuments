# Generated by Django 3.1.13 on 2024-05-23 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturations', '0004_mig14'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestrictionDocument',
            fields=[
                ('id_restric', models.AutoField(db_column='id_dmd', primary_key=True, serialize=False)),
                ('id_user', models.IntegerField()),
                ('id_doc', models.IntegerField()),
                ('acces', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'Restriction',
            },
        ),
    ]