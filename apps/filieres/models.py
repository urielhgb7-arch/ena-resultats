from django.db import models


class AnneeAcademique(models.Model):
    libelle = models.CharField(max_length=50, unique=True, help_text="Ex: 2023-2024")
    en_cours = models.BooleanField(default=False)

    def __str__(self):
        return self.libelle


class Niveau(models.Model):
    libelle = models.CharField(max_length=50, unique=True, help_text="Ex: L1, L2, L3")
    ordre = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.libelle


class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    a_des_specialites = models.BooleanField(default=False)
    specialite_unique_auto = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Specialite(models.Model):
    filiere = models.ForeignKey(
        Filiere, on_delete=models.CASCADE, related_name="specialites"
    )
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.filiere.nom} - {self.nom}"

    class Meta:
        unique_together = ("filiere", "nom")


class Semestre(models.Model):
    numero = models.PositiveIntegerField(help_text="1 pour S1, 2 pour S2, etc.")
    niveau = models.ForeignKey(
        Niveau, on_delete=models.CASCADE, related_name="semestres"
    )

    def __str__(self):
        return f"S{self.numero} ({self.niveau.libelle})"

    class Meta:
        unique_together = ("numero", "niveau")
