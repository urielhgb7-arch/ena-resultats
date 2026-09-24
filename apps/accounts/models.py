from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UtilisateurAdminManager(BaseUserManager):
    def create_user(self, email, nom, role, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nom, role='super_admin', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, nom, role, password, **extra_fields)


class UtilisateurAdmin(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('visiteur', 'Visiteur'),
        ('validateur', 'Validateur'),
        ('super_admin', 'Super Admin'),
    ]

    nom = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=200)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='visiteur')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UtilisateurAdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'role']

    class Meta:
        db_table = 'utilisateur_admin'

    def __str__(self):
        return f"{self.nom} ({self.email})"
