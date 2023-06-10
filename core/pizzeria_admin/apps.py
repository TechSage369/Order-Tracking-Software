from django.apps import AppConfig


class PizzeriaAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pizzeria_admin'

    def ready(self) -> None:
        import pizzeria_admin.signals
