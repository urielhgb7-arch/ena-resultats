from django.db import models
from apps.core.models import Niveau, Semestre


class Filiere(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)
    a_des_specialites = models.BooleanField(
        default=True,
        help_text="Décocher si la filière n'a pas de spécialités (ex: Secrétariat de Direction)",
    )
    specialite_unique_auto = models.BooleanField(
        default=False,
        help_text="Si vrai et qu'il n'y a pas de spécialités, une spécialité 'Tronc Commun' ou du nom de la filière est implicite",
    )
    niveaux = models.ManyToManyField(Niveau, related_name="filieres")

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Specialite(models.Model):
    nom = models.CharField(max_length=150)
    code = models.CharField(max_length=20)
    filiere = models.ForeignKey(
        Filiere, on_delete=models.CASCADE, related_name="specialites"
    )

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        unique_together = ("nom", "filiere")
        ordering = ["filiere", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.filiere.nom})"


class UE(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    credits = models.PositiveSmallIntegerField(default=0)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="ues")
    specialite = models.ForeignKey(
        Specialite, on_delete=models.CASCADE, related_name="ues", null=True, blank=True
    )
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="ues")

    class Meta:
        verbose_name = "Unité d'Enseignement (UE)"
        verbose_name_plural = "Unités d'Enseignement (UE)"
        unique_together = ("code", "semestre", "filiere", "specialite")

    def __str__(self):
        return f"{self.code} - {self.nom}"


class EC(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="ecs")

    class Meta:
        verbose_name = "Élément Constitutif (EC)"
        verbose_name_plural = "Éléments Constitutifs (EC)"
        unique_together = ("code", "ue")

    def __str__(self):
        return f"{self.code} - {self.nom}"
