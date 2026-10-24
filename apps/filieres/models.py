from django.db import models

class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=9, unique=True, help_text="Ex: 2023-2024")
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.annee

class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True, help_text="Ex: L1, L2, L3")
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom

class Filiere(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    a_des_specialites = models.BooleanField(default=True)
    specialite_unique_auto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} ({self.code})"

class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='specialites')
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('filiere', 'code')

    def __str__(self):
        return f"{self.filiere.code} - {self.nom} ({self.code})"

class Semestre(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='semestres')

    class Meta:
        unique_together = ('nom', 'niveau')

    def __str__(self):
        return f"{self.niveau.nom} - {self.nom}"
