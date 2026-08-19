from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UtilisateurAdminManager(BaseUserManager):
    def create_user(self, email, nom, role="visiteur", password=None):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        user = self.model(
            email=self.normalize_email(email),
            nom=nom,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, password=None):
        user = self.create_user(
            email,
            nom=nom,
            role="super_admin",
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UtilisateurAdmin(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("visiteur", "Visiteur"),
        ("validateur", "Validateur"),
        ("super_admin", "Super Administrateur"),
    ]
    nom = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="visiteur")
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UtilisateurAdminManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']
    
    class Meta:
        db_table = "utilisateur_admin"
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        
    def __str__(self):
        return f"{self.nom} ({self.email})"

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(pre_save, sender=UtilisateurAdmin)
def set_permissions_by_role(sender, instance, **kwargs):
    if instance.role == "super_admin":
        instance.is_superuser = True
        instance.is_staff = True
    elif instance.role == "validateur":
        instance.is_superuser = False
        instance.is_staff = True
    else:
        instance.is_superuser = False
        instance.is_staff = False

@receiver(post_save, sender=UtilisateurAdmin)
def assign_group_by_role(sender, instance, created, **kwargs):
    # Ensure the Validateurs group exists
    group, _ = Group.objects.get_or_create(name="Validateurs")
    if instance.role == "validateur":
        instance.groups.add(group)
    else:
        if group in instance.groups.all():
            instance.groups.remove(group)

