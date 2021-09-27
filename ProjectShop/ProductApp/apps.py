from django.apps import AppConfig


class ProductappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProductApp'

    def ready(self):
        import ProductApp.signals

