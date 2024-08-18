from django.apps import AppConfig


class ArchivedocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'archivedocuments'
    def ready(self):
        import archivedocuments.signals
