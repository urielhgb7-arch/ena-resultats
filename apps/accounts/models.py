from django.contrib.auth.models import AbstractUser
from django.db import models

class UtilisateurAdmin(AbstractUser):
    # Les champs par defaut (username, email, password, etc) sont inclus via AbstractUser
    # On ajoute juste les flags pour respecter les regles de securite et de roles s'ils sont necessaires plus tard.
    pass
