from django.apps import AppConfig


class WeioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weio'

    def ready(self):
        from . import signals
