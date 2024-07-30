from django.apps import AppConfig


class FacturationsConfig(AppConfig):
    name = 'facturations'

    def ready(self):
        import facturations.signals