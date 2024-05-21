# Generated by Django 3.1.13 on 2024-05-18 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturations', '0001_mig11'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemandePermission',
            fields=[
                ('id_dmd_per', models.AutoField(db_column='id_dmd', primary_key=True, serialize=False)),
                ('motif_dmd', models.CharField(max_length=255)),
                ('commentaire_vld', models.CharField(max_length=255, null=True)),
                ('date_dmd', models.DateField(auto_now_add=True)),
                ('id_demandeur', models.IntegerField(db_column='id_demandeur')),
                ('id_valideur', models.IntegerField(db_column='id_acepteur', null=True)),
                ('etat', models.IntegerField(default=0)),
                ('id_per', models.IntegerField(db_column='id_per')),
                ('id_document', models.IntegerField(db_column='id_docuemnt')),
            ],
            options={
                'db_table': 'DemandePermission',
            },
        ),
        migrations.RemoveField(
            model_name='document',
            name='numero_bl',
        ),
        migrations.AddField(
            model_name='demande',
            name='commentaire_reponse',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='demande',
            name='id_accepteur',
            field=models.IntegerField(db_column='id_acepteur', null=True),
        ),
        migrations.AlterField(
            model_name='demande',
            name='id_boite',
            field=models.IntegerField(db_column='id_boite', null=True),
        ),
        migrations.AlterField(
            model_name='demande',
            name='id_docuement',
            field=models.IntegerField(db_column='id_document', null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='chemin_acces',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='document',
            name='client',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='eta',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='id_boite',
            field=models.IntegerField(db_column='id_boite', null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='id_per',
            field=models.IntegerField(db_column='id_per', default=2, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='id_us',
            field=models.IntegerField(db_column='id_us', null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='nom_navire',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='numero_voyage',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='permissions',
            name='id_user',
            field=models.IntegerField(db_column='id_us', default=0),
        ),
    ]