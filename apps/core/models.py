from django.db import models


class AnneeAcademique(models.Model):
    libelle = models.CharField(max_length=20)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = "annee_academique"

    def __str__(self):
        return self.libelle


class Niveau(models.Model):
    annee = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=10)

    class Meta:
        db_table = "niveau"

    def __str__(self):
        return f"{self.libelle} ({self.annee.libelle})"


class Semestre(models.Model):
    filiere = models.ForeignKey("filieres.Filiere", on_delete=models.CASCADE)
    libelle = models.CharField(max_length=20)
    type = models.CharField(max_length=30, default="normal")

    class Meta:
        db_table = "semestre"

    def __str__(self):
        return f"{self.libelle} - {self.filiere.nom}"


class SessionResultat(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    specialite = models.ForeignKey(
        "filieres.Specialite", on_delete=models.SET_NULL, null=True, blank=True
    )
    type = models.CharField(max_length=30)

    class Meta:
        db_table = "session_resultat"

    def __str__(self):
        return f"{self.type} - {self.semestre.libelle}"
