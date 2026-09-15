from django.db import models


class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=9, unique=True, help_text="Ex: 2023-2024")
    est_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Année académique"
        verbose_name_plural = "Années académiques"

    def __str__(self):
        return self.annee


class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True, help_text="Ex: L1, L2, M1")
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ["ordre"]

    def __str__(self):
        return self.nom


class Semestre(models.Model):
    nom = models.CharField(max_length=50, help_text="Ex: Semestre 1")
    niveau = models.ForeignKey(
        Niveau, on_delete=models.CASCADE, related_name="semestres"
    )
    numero = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        unique_together = ("nom", "niveau")
        ordering = ["numero"]

    def __str__(self):
        return f"{self.nom} ({self.niveau.nom})"


class SessionResultat(models.Model):
    class TypeSession(models.TextChoices):
        NORMALE = "NORMALE", "Normale"
        RATTRAPAGE = "RATTRAPAGE", "Rattrapage"
        AJOURNEMENT = "AJOURNEMENT", "Ajournement"

    nom = models.CharField(max_length=100)
    type_session = models.CharField(
        max_length=20, choices=TypeSession.choices, default=TypeSession.NORMALE
    )
    annee_academique = models.ForeignKey(
        AnneeAcademique, on_delete=models.CASCADE, related_name="sessions"
    )
    semestre = models.ForeignKey(
        Semestre, on_delete=models.CASCADE, related_name="sessions"
    )

    class Meta:
        verbose_name = "Session de résultat"
        verbose_name_plural = "Sessions de résultat"
        unique_together = ("type_session", "annee_academique", "semestre")

    def __str__(self):
        return f"{self.nom} - {self.annee_academique} - {self.semestre}"
