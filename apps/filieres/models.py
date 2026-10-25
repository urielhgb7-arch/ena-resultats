from django.db import models


class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=9, unique=True)  # ex: "2023-2024"


class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True)  # ex: "Licence 1"


class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    a_des_specialites = models.BooleanField(default=False)
    specialite_unique_auto = models.BooleanField(default=False)


class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)


class Semestre(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)


class UE(models.Model):
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    credits = models.IntegerField()


class EC(models.Model):
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
