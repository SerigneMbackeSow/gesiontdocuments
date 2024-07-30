from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from facturations.models import Utilisateurs

@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    if sender.name == 'facturations':
        ################# CREATION DES UTILISATEURS AU DEMARRAGE DE L'APPLICATION ################
        #  POUR LE SUPER ADMIN #
        if not Utilisateurs.objects.filter( role='admin').exists():
            Utilisateurs.objects.create(prenom='Super', nom='Admin', password='1234', email='superadmin',  role='Admin', direction='ADMIN')
        #  POUR LE CHEF DE SERVICE FACTURATION #
        if not Utilisateurs.objects.filter( role='chef', direction='facturation').exists():
            Utilisateurs.objects.create(prenom='Seydou', nom='Niang', password='1234', email='sniang',  role='chef', direction='facturation')
        #  POUR LE CHEF DE SERVICE DOCUMENTION #
        if not Utilisateurs.objects.filter(role='chef', direction='documentation').exists():
            Utilisateurs.objects.create(prenom='Edmond', nom='Dacosta', password='1234', email='edacosta', role='chef',
                                            direction='documentation')
            #  POUR LE CHEF DE SERVICE ARCHIVE #
        if not Utilisateurs.objects.filter( role='chef', direction='archive').exists():
            Utilisateurs.objects.create(prenom='Chef', nom='Archive', password='1234', email='carchive',  role='chef', direction='archive')
            #  POUR LE CHEF DE SERVICE TRANSFERT #
        if not Utilisateurs.objects.filter( role='chef', direction='transfert').exists():
            Utilisateurs.objects.create(prenom='Saliou', nom='Sagna', password='1234', email='ssagna',  role='chef', direction='transfert')
        if not Utilisateurs.objects.filter(direction='management').exists():
            Utilisateurs.objects.create(prenom='Management1', nom='Management1', password='1234', email='management1', role='chef',
                                        direction='management')
            Utilisateurs.objects.create(prenom='Management2', nom='Management2', password='1234', email='management2',
                                        role='chef',
                                        direction='management')