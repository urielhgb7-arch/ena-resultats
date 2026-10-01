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

class Semestre(models.Model):
    filiere = models.ForeignKey('filieres.Filiere', on_delete=models.CASCADE)
    libelle = models.CharField(max_length=20)
    type = models.CharField(max_length=30, default='normal')

    class Meta:
        db_table = 'semestre'

class SessionResultat(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    specialite = models.ForeignKey('filieres.Specialite', null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=30)

    class Meta:
        db_table = 'session_resultat'
