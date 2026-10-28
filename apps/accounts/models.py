from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UtilisateurAdmin(AbstractUser):
    class Role(models.TextChoices):
        VISITEUR = 'visiteur', _('Visiteur (public)')
        VALIDATEUR = 'validateur', _('Validateur/Administrateur')
        SUPER_ADMIN = 'super_admin', _('Super-administrateur')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VISITEUR,
    )

    class Meta:
        verbose_name = _('Utilisateur Admin')
        verbose_name_plural = _('Utilisateurs Admin')
        db_table = 'accounts_utilisateuradmin'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
