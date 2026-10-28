from django.db import models
from django.utils.translation import gettext_lazy as _

class AnneeAcademique(models.Model):
    libelle = models.CharField(max_length=20, unique=True, help_text="Ex: 2023-2024")
    en_cours = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Année Académique")
        verbose_name_plural = _("Années Académiques")
        db_table = 'filieres_anneeacademique'

    def __str__(self):
        return self.libelle

class Niveau(models.Model):
    libelle = models.CharField(max_length=50, unique=True, help_text="Ex: L1, L2, L3, M1, M2")
    ordre = models.IntegerField(default=1)

    class Meta:
        verbose_name = _("Niveau")
        verbose_name_plural = _("Niveaux")
        ordering = ['ordre']
        db_table = 'filieres_niveau'

    def __str__(self):
        return self.libelle

class Filiere(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    a_des_specialites = models.BooleanField(default=False)
    specialite_unique_auto = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Filière")
        verbose_name_plural = _("Filières")
        db_table = 'filieres_filiere'

    def __str__(self):
        return self.nom

class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="specialites")
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Spécialité")
        verbose_name_plural = _("Spécialités")
        unique_together = ('filiere', 'code')
        db_table = 'filieres_specialite'

    def __str__(self):
        return f"{self.filiere.code} - {self.nom}"

class Semestre(models.Model):
    numero = models.IntegerField()
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="semestres")

    class Meta:
        verbose_name = _("Semestre")
        verbose_name_plural = _("Semestres")
        unique_together = ('numero', 'niveau')
        ordering = ['niveau__ordre', 'numero']
        db_table = 'filieres_semestre'

    def __str__(self):
        return f"S{self.numero} ({self.niveau.libelle})"
