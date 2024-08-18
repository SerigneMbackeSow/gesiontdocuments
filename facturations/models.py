from datetime import datetime

from users.models import User
from django.db import models

class Utilisateurs(models.Model):
    id_utilisateur = models.AutoField(primary_key=True, db_column='id_user')
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255,null=True)
    email = models.EmailField(unique=True,null=False)
    password = models.CharField(max_length=255,null=False)
    etat = models.IntegerField(default=1)
    telephone = models.CharField(max_length=15,null=True)
    direction = models.CharField(max_length=255,null=False)
    role = models.CharField(max_length=255, null=False)
    class Meta:
     db_table = 'Utilisateur'


class UniteStockage():
    id_us = models.AutoField(primary_key=True, db_column='id_us')
    type = models.CharField(max_length=255)
    mention = models.CharField(max_length=255)
    date_creation=models.DateField()
    id_user = models.IntegerField(db_column='id_user')
    class Meta:
        db_table = 'UniteStockage'


class Boite(models.Model):
    id_boite=models.AutoField(primary_key=True, db_column='id_boite')
    mention = models.CharField( max_length=150)
    numero_rang= models.CharField(max_length=150,default="Aucune")
    date_creation = models.DateField(auto_now_add=True)
    id_user = models.IntegerField(db_column='id_user')
    etat = models.IntegerField(default=1)
    harmoire = models.CharField(max_length=150,default="Aucune")
    numero_comp = models.CharField(max_length=50,default="Aucune")
    niveau = models.CharField(max_length=50,default="Aucune")
    commentaire = models.CharField(max_length=255,default="Aucun")

    class Meta:
        db_table = 'Boite'




class Document(models.Model):
    id_document= models.AutoField(primary_key=True, db_column='id_document')
    numero_docuemnt = models.CharField( max_length=150)
    date_creation = models.DateField(auto_now_add=True)
    date_destruction = models.DateField(null=True)
    bl = models.CharField(max_length=255,null=True,default='BL')
    chemin_acces = models.CharField(max_length=255)
    disponibilite = models.IntegerField(default=0)
    #eta = models.CharField(null=True,max_length=10)
    #eta=models.DateField(default=datetime.now())
    eta=models.DateTimeField(null=True)
    client = models.CharField(null=True,max_length=40)
    nom_navire = models.CharField(null=True,max_length=100)
    numero_voyage = models.CharField(null=True,max_length=100)
    id_us = models.IntegerField(null=True,db_column='id_us')
    id_boite = models.IntegerField(null=True,db_column='id_boite')
    id_per = models.IntegerField(null=True, db_column='id_per',default=2)

    class Meta:
        db_table = 'Document'


class Demande(models.Model):
    id_dmd = models.AutoField(primary_key=True, db_column='id_dmd')
    type = models.CharField(max_length=150)
    commentaire = models.CharField(max_length=255)
    commentaire_reponse= models.CharField(null=True,max_length=255)
    date_dmd = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True)
    id_demandeur = models.IntegerField(db_column='id_demandeur')
    id_accepteur = models.IntegerField(null=True,db_column='id_acepteur')
    etat = models.IntegerField(default=0)
    id_docuement = models.IntegerField(null=True,db_column='id_document')
    id_boite = models.IntegerField(null=True,db_column='id_boite')

    class Meta:
        db_table = 'Demande'
class RestrictionDocument(models.Model):
        id_restric = models.AutoField(primary_key=True, db_column='id_dmd')
        id_user=models.IntegerField()
        id_doc=models.IntegerField()
        #####A remplacer
        numero_docuent=models.CharField(max_length=255,default='numero_doc')
        service=models.CharField(max_length=255,default='service')
        date_dmd=models.DateField(null=True)
        etat = models.IntegerField(default=1)
        dmd = models.IntegerField(default=0)
        ref = models.IntegerField(default=0)
        acces_dir = models.IntegerField(default=0)
        acces=models.CharField(max_length=150)
        id_chef = models.IntegerField(default=0)
        class Meta:
            db_table = 'Restriction'

