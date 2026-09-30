from django.db import models
from django.contrib.auth.models import AbstractUser


class UtilisateurAdmin(AbstractUser):
    # Les rôles (Visiteur, Validateur, Super-admin) seront gérés par les Groupes/Permissions natifs ou via guardian plus tard,
    # ou on peut ajouter un champ simple si on préfère. Laissons AbstractUser tel quel pour l'instant avec les champs par défaut.
    pass
