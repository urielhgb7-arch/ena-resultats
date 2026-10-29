from django.db import models
from django.utils.translation import gettext_lazy as _

class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=9, unique=True, help_text="Ex: 2023-2024")

    def __str__(self):
        return self.annee

    class Meta:
        verbose_name = _('Année Académique')
        verbose_name_plural = _('Années Académiques')

class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = _('Niveau')
        verbose_name_plural = _('Niveaux')

class Filiere(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    a_des_specialites = models.BooleanField(default=False)
    specialite_unique_auto = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = _('Filière')
        verbose_name_plural = _('Filières')

class Specialite(models.Model):
    nom = models.CharField(max_length=255)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='specialites')

    def __str__(self):
        return f"{self.filiere.nom} - {self.nom}"

    class Meta:
        verbose_name = _('Spécialité')
        verbose_name_plural = _('Spécialités')
        unique_together = ('nom', 'filiere')

class Semestre(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='semestres')

    def __str__(self):
        return f"{self.niveau.nom} - {self.nom}"

    class Meta:
        verbose_name = _('Semestre')
        verbose_name_plural = _('Semestres')
        unique_together = ('nom', 'niveau')

class UE(models.Model):
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    credits = models.PositiveIntegerField()
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='ues')
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='ues')
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, related_name='ues', null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.nom}"

    class Meta:
        verbose_name = _('Unité d\'Enseignement')
        verbose_name_plural = _('Unités d\'Enseignement')

class EC(models.Model):
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='ecs')

    def __str__(self):
        return f"{self.code} - {self.nom}"

    class Meta:
        verbose_name = _('Élément Constitutif')
        verbose_name_plural = _('Éléments Constitutifs')
