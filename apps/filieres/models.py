from django.db import models


class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=9, unique=True, help_text="Ex: 2023-2024")
    en_cours = models.BooleanField(default=False)

    def __str__(self):
        return self.annee


class Niveau(models.Model):
    nom = models.CharField(
        max_length=50, unique=True, help_text="Ex: L1, L2, L3, M1, M2"
    )
    ordre = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.nom


class Filiere(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    a_des_specialites = models.BooleanField(default=False)
    specialite_unique_auto = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Specialite(models.Model):
    filiere = models.ForeignKey(
        Filiere, on_delete=models.CASCADE, related_name="specialites"
    )
    nom = models.CharField(max_length=255)

    class Meta:
        unique_together = ("filiere", "nom")

    def __str__(self):
        return f"{self.filiere.nom} - {self.nom}"


class Semestre(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.ForeignKey(
        Niveau, on_delete=models.CASCADE, related_name="semestres"
    )

    def __str__(self):
        return f"{self.nom} ({self.niveau.nom})"


class UE(models.Model):
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=255)
    credits = models.PositiveSmallIntegerField(default=1)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="ues")
    specialite = models.ForeignKey(
        Specialite, on_delete=models.CASCADE, related_name="ues", null=True, blank=True
    )

    def __str__(self):
        return f"{self.code} - {self.nom}"


class EC(models.Model):
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=255)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="ecs")

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=150)
    filiere = models.ForeignKey(
        Filiere, on_delete=models.SET_NULL, null=True, related_name="etudiants"
    )
    specialite = models.ForeignKey(
        Specialite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="etudiants",
    )
    niveau_actuel = models.ForeignKey(
        Niveau, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"
