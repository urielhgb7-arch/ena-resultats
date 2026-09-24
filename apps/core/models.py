from django.db import models


class AnneeAcademique(models.Model):
    libelle = models.CharField(max_length=20)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'annee_academique'

    def __str__(self):
        return self.libelle


class Niveau(models.Model):
    annee = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=10)

    class Meta:
        db_table = 'niveau'

    def __str__(self):
        return f"{self.libelle} ({self.annee})"
