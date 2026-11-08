from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UtilisateurAdmin(AbstractUser):
    class Role(models.TextChoices):
        VISITEUR = 'VISITEUR', _('Visiteur')
        VALIDATEUR = 'VALIDATEUR', _('Validateur')
        SUPER_ADMIN = 'SUPER_ADMIN', _('Super-administrateur')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VISITEUR,
        help_text=_('Role of the user on the platform.')
    )

    class Meta:
        verbose_name = _('Utilisateur Admin')
        verbose_name_plural = _('Utilisateurs Admin')
