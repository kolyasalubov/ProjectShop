from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "UserApp"

    def ready(self):
        import signals.signals  # noqa: F401
