from django.db import models

class AnneeAcademique(models.Model):
    libelle = models.CharField(max_length=20)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'annee_academique'

class Niveau(models.Model):
    annee = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=10)

    class Meta:
        db_table = 'niveau'

class Filiere(models.Model):
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    a_des_specialites = models.BooleanField(default=True)
    specialite_unique_auto = models.BooleanField(default=False)

    class Meta:
        db_table = 'filiere'

class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)

    class Meta:
        db_table = 'specialite'

class Semestre(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=20)
    type = models.CharField(max_length=30, default='normal')

    class Meta:
        db_table = 'semestre'
