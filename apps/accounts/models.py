from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class UtilisateurAdmin(AbstractUser):
    class Role(models.TextChoices):
        VALIDATEUR = 'VALIDATEUR', _('Validateur/Administrateur')
        SUPER_ADMIN = 'SUPER_ADMIN', _('Super-administrateur')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VALIDATEUR,
        blank=True
    )

    class Meta:
        verbose_name = _('Utilisateur Admin')
        verbose_name_plural = _('Utilisateurs Admin')
