from django.db.models.signals import post_migrate
from django.dispatch import receiver
from archivedocuments.models import Dossiers,Direction
@receiver(post_migrate)
def create_default_direction(sender, **kwargs):
    if sender.name == 'archivedocuments':
        default_directions = ['admin', 'facturation', 'documentation', 'management']

        for direction_name in default_directions:
            if not Direction.objects.filter(nom=direction_name).exists():
                Direction.objects.create(nom=direction_name)
            if not Dossiers.objects.filter(id_parent__isnull=True).exists():
                Dossiers.objects.create(nom='TOM')