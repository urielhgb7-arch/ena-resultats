from django.db import models
from django.utils.translation import gettext_lazy as _

class AnneeAcademique(models.Model):
    libelle = models.CharField(max_length=50, unique=True, help_text=_("e.g. 2023-2024"))
    en_cours = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Année académique')
        verbose_name_plural = _('Années académiques')

    def __str__(self):
        return self.libelle

class Niveau(models.Model):
    libelle = models.CharField(max_length=50, unique=True, help_text=_("e.g. Licence 1"))
    code = models.CharField(max_length=10, unique=True, help_text=_("e.g. L1"))

    class Meta:
        verbose_name = _('Niveau')
        verbose_name_plural = _('Niveaux')

    def __str__(self):
        return f"{self.libelle} ({self.code})"

class Filiere(models.Model):
    libelle = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    a_des_specialites = models.BooleanField(default=False)
    specialite_unique_auto = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Filière')
        verbose_name_plural = _('Filières')

    def __str__(self):
        return f"{self.libelle} ({self.code})"

class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='specialites')
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    class Meta:
        verbose_name = _('Spécialité')
        verbose_name_plural = _('Spécialités')
        unique_together = ('filiere', 'code')

    def __str__(self):
        return f"{self.filiere.code} - {self.libelle} ({self.code})"

class Semestre(models.Model):
    libelle = models.CharField(max_length=50)
    numero = models.PositiveIntegerField()
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='semestres')

    class Meta:
        verbose_name = _('Semestre')
        verbose_name_plural = _('Semestres')
        unique_together = ('niveau', 'numero')

    def __str__(self):
        return f"{self.libelle} (S{self.numero})"
