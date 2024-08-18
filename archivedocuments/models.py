from django.db import models

# Create your models here.
import datetime
from django.shortcuts import render
# Create your views here.
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
##################### Model Dossier #########################
class Dossiers(models.Model):
    id_dossier = models.AutoField(primary_key=True)
    date_creation = models.DateTimeField(null=True, blank=True)
    nom = models.CharField(max_length=255, null=True)
    direction = models.CharField(max_length=255, null=True)
    id_parent = models.IntegerField(null=True)
    def get_type(self):
        return 'dossiers'




##################### Model Utilisateur #########################

class Utilisateur(models.Model):
    id_user = models.AutoField(primary_key=True, db_column='id_user')
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True,null=False)
    password = models.CharField(max_length=255,null=False)
    direction = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=255, null=False)
    status=models.CharField(max_length=255,default='active')
    def str(self):
        return f"Utilisateur {self.id_user}"
    ##################### Model Document #########################

class Documents(models.Model):
    id_document= models.AutoField(primary_key=True, db_column='id_document')
    numero_document = models.CharField( max_length=150)
    date_creation = models.DateTimeField(null=True, blank=True)
    bl = models.CharField(max_length=255,null=True)
    nom = models.CharField(max_length=255)
    eta = models.DateTimeField(null=True)
    client = models.CharField(null=True,max_length=40)
    vessel = models.CharField(null=True,max_length=100)
    numero_voyage = models.CharField(null=True,max_length=100)
    conteneur = models.CharField(null=True, max_length=100)
    montant = models.CharField(null=True, max_length=100)
    journal = models.CharField(null=True, max_length=100)
    montant = models.FloatField(null=True)
    id_parent = models.IntegerField(null=False,db_column='parent')
    direction = models.CharField(max_length=255,null=True)

    def get_type(self):
        return 'documents'

    def __str__(self):
        return self.nom
    class Meta:
        db_table = 'Documents'

    ##################### Model Demande #########################
class Demandes(models.Model):
    id_dmd = models.AutoField(primary_key=True, db_column='id_dmd')
    type = models.CharField(max_length=150)
    commentaire = models.CharField(max_length=255)
    commentaire_reponse= models.CharField(null=True,max_length=255)
    date_dmd = models.DateField(auto_now_add=True)
    id_demandeur = models.IntegerField(db_column='id_demandeur')
    id_recepteur = models.IntegerField(null=True,db_column='id_recepteur')
    etat = models.IntegerField(default=0)
    id_objet = models.IntegerField(null=False, db_column='id_objet')
    class Meta:
        db_table = 'Demandes'
    ##################### Model Acces #########################
class Acces(models.Model):
    id_per = models.AutoField(primary_key=True, db_column='id_dmd')
    type = models.CharField(max_length=150)
    permission = models.CharField(max_length=255)
    id_utilisateur = models.IntegerField(null=True, db_column='id_utilisateur')
    etat = models.IntegerField(default=0)
    id_objet = models.IntegerField(null=False, db_column='id_objet')
    class Meta:
        db_table = 'Acces'

class Direction(models.Model):
    id_direction = models.AutoField(primary_key=True, db_column='id_dmd')
    nom = models.CharField(max_length=255)
    class Meta:
        db_table = 'direction'