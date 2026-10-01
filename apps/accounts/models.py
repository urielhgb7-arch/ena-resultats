from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UtilisateurAdminManager(BaseUserManager):
    def create_user(self, email, nom, role, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            nom=nom,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, role, password=None):
        user = self.create_user(
            email,
            password=password,
            nom=nom,
            role=role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UtilisateurAdmin(AbstractBaseUser):
    ROLE_CHOICES = (
        ('visiteur', 'Visiteur'),
        ('validateur', 'Validateur'),
        ('super_admin', 'Super Admin'),
    )
    nom = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UtilisateurAdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'role']

    class Meta:
        db_table = 'utilisateur_admin'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
