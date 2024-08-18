# Generated by Django 5.0.6 on 2024-08-10 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acces',
            fields=[
                ('id_per', models.AutoField(db_column='id_dmd', primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=150)),
                ('permission', models.CharField(max_length=255)),
                ('id_utilisateur', models.IntegerField(db_column='id_utilisateur', null=True)),
                ('etat', models.IntegerField(default=0)),
                ('id_objet', models.IntegerField(db_column='id_objet')),
            ],
            options={
                'db_table': 'Acces',
            },
        ),
        migrations.CreateModel(
            name='Demandes',
            fields=[
                ('id_dmd', models.AutoField(db_column='id_dmd', primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=150)),
                ('commentaire', models.CharField(max_length=255)),
                ('commentaire_reponse', models.CharField(max_length=255, null=True)),
                ('date_dmd', models.DateField(auto_now_add=True)),
                ('id_demandeur', models.IntegerField(db_column='id_demandeur')),
                ('id_recepteur', models.IntegerField(db_column='id_recepteur', null=True)),
                ('etat', models.IntegerField(default=0)),
                ('id_objet', models.IntegerField(db_column='id_objet')),
            ],
            options={
                'db_table': 'Demandes',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id_direction', models.AutoField(db_column='id_dmd', primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'direction',
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id_document', models.AutoField(db_column='id_document', primary_key=True, serialize=False)),
                ('numero_document', models.CharField(max_length=150)),
                ('date_creation', models.DateTimeField(blank=True, null=True)),
                ('bl', models.CharField(max_length=255, null=True)),
                ('nom', models.CharField(max_length=255)),
                ('eta', models.DateTimeField(null=True)),
                ('client', models.CharField(max_length=40, null=True)),
                ('vessel', models.CharField(max_length=100, null=True)),
                ('numero_voyage', models.CharField(max_length=100, null=True)),
                ('conteneur', models.CharField(max_length=100, null=True)),
                ('journal', models.CharField(max_length=100, null=True)),
                ('montant', models.FloatField(null=True)),
                ('id_parent', models.IntegerField(db_column='parent')),
            ],
            options={
                'db_table': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Dossiers',
            fields=[
                ('id_dossier', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(blank=True, null=True)),
                ('nom', models.CharField(max_length=255, null=True)),
                ('direction', models.CharField(max_length=255, null=True)),
                ('id_parent', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id_user', models.AutoField(db_column='id_user', primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('direction', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('status', models.CharField(default='active', max_length=255)),
            ],
        ),
    ]
