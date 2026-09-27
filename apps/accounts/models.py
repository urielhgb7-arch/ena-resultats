from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UtilisateurAdminManager(BaseUserManager):
    def create_user(self, email, nom, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UtilisateurAdmin.Role.SUPER_ADMIN)

        return self.create_user(email, nom, password, **extra_fields)


class UtilisateurAdmin(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        VISITEUR = "visiteur", "Visiteur"
        VALIDATEUR = "validateur", "Validateur"
        SUPER_ADMIN = "super_admin", "Super-administrateur"

    nom = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, unique=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.VISITEUR)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UtilisateurAdminManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom"]

    class Meta:
        db_table = "utilisateur_admin"

    def __str__(self):
        return f"{self.nom} ({self.email})"
