from django.db import models
from django.contrib.auth.models import AbstractUser

class UtilisateurAdmin(AbstractUser):
    # Optional: we can add extra fields here according to the schema
    # For now, it satisfies the required AUTH_USER_MODEL for Django
    pass
