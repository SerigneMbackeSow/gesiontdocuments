
from users.models import User
from django.db import models

class Utilisateurs(models.Model):
    id_utilisateur = models.AutoField(primary_key=True, db_column='id_user')
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255,null=True)
    email = models.EmailField(unique=True,null=False)
    password = models.CharField(max_length=255,null=False)
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

    class Meta:
        db_table = 'Boite'


class Document(models.Model):
    id_document= models.AutoField(primary_key=True, db_column='id_document')
    numero_docuemnt = models.CharField( max_length=150)
    date_creation = models.DateField(auto_now_add=True)
    date_destruction = models.DateField(null=True)
    chemin_acces = models.CharField(max_length=255)
    disponibilite = models.IntegerField(default=0)
    eta = models.CharField(null=True,max_length=10)
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


class DemandePermission(models.Model):
    id_dmd_per= models.AutoField(primary_key=True, db_column='id_dmd')
    motif_dmd = models.CharField(max_length=255)
    commentaire_vld= models.CharField(null=True,max_length=255)
    date_dmd = models.DateField(auto_now_add=True)
    id_demandeur = models.IntegerField(db_column='id_demandeur')
    id_valideur = models.IntegerField(null=True,db_column='id_acepteur')
    etat = models.IntegerField(default=0)
    id_per = models.IntegerField(db_column='id_per')
    id_document = models.IntegerField(db_column='id_docuemnt')

    class Meta:
        db_table = 'DemandePermission'


class Permissions(models.Model):
    id_permission = models.AutoField(primary_key=True, db_column='id_per')
    type=models.IntegerField(default=0)
    description = models.CharField(max_length=255)
    id_user= models.IntegerField(default=0,db_column='id_us')
    class Meta:
        db_table = 'Permission'


class DetailsDossier(models.Model):

    id_dossier= models.CharField(primary_key=True,max_length=15)
    numero_bl=models.CharField(max_length=15)
    eta=models.CharField(max_length=15)
    nom_navire=models.CharField(max_length=50)
    numero_voyage=models.CharField(max_length=50)
    localisation=models.CharField(max_length=50)
    numer_boite=models.CharField(max_length=50)
    carton=models.CharField(max_length=50)
    classeur=models.CharField(max_length=50)
    class Meta:
        db_table = 'Details_dossier'


class Permission(models.Model):

    id_permission = models.AutoField(primary_key=True)
    class ModuleChoices(models.TextChoices):
        FACTURATION = 'Facturation'
        COMPTABILITE =  'Comptabilité'
        EXPLOITATAIN='Exploitation'
        DOCUMENTATION = 'Documentation'
    class PrivilegeChoices(models.TextChoices):
        AJOUTER ='Ajouter'
        MODIFIER ='Modifier'
        SUPPRIMER ='Supprimer'
        CONSULTER ='Consulter'
    module = models.CharField(max_length=50,choices=ModuleChoices.choices)
    privelege = models.CharField(max_length=50,choices=PrivilegeChoices.choices)
    nom_acces = models.CharField(max_length=255)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Permissionn'
    def __str__(self):
        return f"{self.module} - {self.privelege} - {self.nom_acces}"

class Archive(models.Model):
    numero_dossier = models.CharField(primary_key=True, max_length=150)
    localisation = models.CharField(max_length=50)
    numer_boite = models.CharField(max_length=50)
    class Meta:
        db_table = 'Archive'

class Localisation(models.Model):
    id_harmoire = models.CharField( max_length=150)
    numero_comp = models.CharField(max_length=50)
    niveau= models.CharField(max_length=50)
    numero_dossier = models.CharField(primary_key=True,max_length=50)
    id_user = models.IntegerField(db_column='id_user')
    class Meta:
        db_table = 'Localisation'

