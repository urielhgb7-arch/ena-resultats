from django.db import models


class TimestampedModel(models.Model):
    """Mixin reutilisable : ajoute created_at/updated_at a un modele."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
