from django.db import models

class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=9, unique=True, help_text="Ex: 2023-2024")
    en_cours = models.BooleanField(default=False)

    def __str__(self):
        return self.annee

class Filiere(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    a_des_specialites = models.BooleanField(default=True)
    specialite_unique_auto = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='specialites')
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('filiere', 'code')

    def __str__(self):
        return f"{self.filiere.code} - {self.nom}"

class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True) # Ex: L1, L2, L3, M1, M2
    ordre = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.nom

class Semestre(models.Model):
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='semestres')
    nom = models.CharField(max_length=50) # Ex: S1, S2
    numero = models.PositiveIntegerField()

    class Meta:
        unique_together = ('niveau', 'numero')

    def __str__(self):
        return f"{self.niveau.nom} - {self.nom}"

class UE(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='ues')
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, null=True, blank=True, related_name='ues')
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='ues')
    code = models.CharField(max_length=50)
    nom = models.CharField(max_length=255)
    credits = models.PositiveIntegerField()

    class Meta:
        unique_together = ('filiere', 'specialite', 'semestre', 'code')

    def __str__(self):
        return f"{self.code} - {self.nom}"

class EC(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='ecs')
    code = models.CharField(max_length=50)
    nom = models.CharField(max_length=255)
    coefficient = models.FloatField()

    class Meta:
        unique_together = ('ue', 'code')

    def __str__(self):
        return f"{self.code} - {self.nom}"

class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"
