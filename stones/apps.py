from django.apps import AppConfig


class StonesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stones'

    def ready(self):
        import stones.signals