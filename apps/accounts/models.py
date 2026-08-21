from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    VISITEUR = "VISITEUR", "Visiteur"
    VALIDATEUR = "VALIDATEUR", "Validateur"
    SUPER_ADMIN = "SUPER_ADMIN", "Super Administrateur"


class UtilisateurAdmin(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VISITEUR,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
