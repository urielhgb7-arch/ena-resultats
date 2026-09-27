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
        return f"{self.libelle} - {self.annee}"


class Filiere(models.Model):
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    a_des_specialites = models.BooleanField(default=True)
    specialite_unique_auto = models.BooleanField(default=False)

    class Meta:
        db_table = "filiere"

    def __str__(self):
        return self.nom


class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)

    class Meta:
        db_table = "specialite"

    def __str__(self):
        return self.nom


class Semestre(models.Model):
    class TypeSemestre(models.TextChoices):
        NORMAL = "normal", "Normal"
        STAGE = "stage", "Stage"

    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=20)
    type = models.CharField(
        max_length=30, choices=TypeSemestre.choices, default=TypeSemestre.NORMAL
    )

    class Meta:
        db_table = "semestre"

    def __str__(self):
        return self.libelle


class SessionResultat(models.Model):
    class TypeSession(models.TextChoices):
        NORMALE = "normale", "Normale"
        RATTRAPAGE = "rattrapage", "Rattrapage"
        AJOURNEMENT = "ajournement", "Ajournement"
        RE_ENJAMBEMENT = "re_enjambement", "Ré-enjambement"

    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    specialite = models.ForeignKey(
        Specialite, on_delete=models.SET_NULL, null=True, blank=True
    )
    type = models.CharField(max_length=30, choices=TypeSession.choices)

    class Meta:
        db_table = "session_resultat"

    def __str__(self):
        return f"{self.type} - {self.semestre}"
