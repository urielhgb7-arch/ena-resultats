from django.contrib.auth.models import AbstractUser
from django.db import models

class UtilisateurAdmin(AbstractUser):
    # Les rôles seront gérés plus tard via les permissions ou groupes,
    # mais pour l'instant, c'est l'entité de base.
    pass
