from django.apps import AppConfig

class ResultatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.resultats"
    verbose_name = "Résultats"

    def ready(self):
        import apps.resultats.signals
