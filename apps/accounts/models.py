from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UtilisateurAdminManager(BaseUserManager):
    def create_user(self, email, nom, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, role='super_admin', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nom, role, password, **extra_fields)

class UtilisateurAdmin(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('visiteur', 'Visiteur'),
        ('validateur', 'Validateur'),
        ('super_admin', 'Super-administrateur'),
    ]

    nom = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UtilisateurAdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'role']

    class Meta:
        db_table = 'utilisateur_admin'

    def __str__(self):
        return f"{self.nom} ({self.email})"
