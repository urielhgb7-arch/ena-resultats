from django.db import models


class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=9, unique=True, help_text="Ex: 2023-2024")

    def __str__(self):
        return self.annee


class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True, help_text="Ex: L1, L2, L3")

    def __str__(self):
        return self.nom


class Filiere(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    a_des_specialites = models.BooleanField(default=False)
    specialite_unique_auto = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Specialite(models.Model):
    nom = models.CharField(max_length=150)
    filiere = models.ForeignKey(
        Filiere, on_delete=models.CASCADE, related_name="specialites"
    )

    def __str__(self):
        return f"{self.filiere.nom} - {self.nom}"

    class Meta:
        unique_together = ("nom", "filiere")


class Semestre(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.ForeignKey(
        Niveau, on_delete=models.CASCADE, related_name="semestres"
    )

    def __str__(self):
        return f"{self.nom} ({self.niveau.nom})"


class UE(models.Model):
    code = models.CharField(max_length=20, unique=True)
    intitule = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="ues")
    specialite = models.ForeignKey(
        Specialite, on_delete=models.SET_NULL, null=True, blank=True, related_name="ues"
    )

    def __str__(self):
        return f"{self.code} - {self.intitule}"


class EC(models.Model):
    code = models.CharField(max_length=20, unique=True)
    intitule = models.CharField(max_length=200)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="ecs")

    def __str__(self):
        return f"{self.code} - {self.intitule}"
