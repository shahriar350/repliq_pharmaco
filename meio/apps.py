from django.apps import AppConfig


class MeioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meio'

    def ready(self):
        from . import signals
