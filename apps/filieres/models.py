from django.db import models

class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=9, unique=True, help_text="Ex: 2023-2024")
    en_cours = models.BooleanField(default=False)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return self.annee

class Niveau(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="Ex: L1, L2, L3, M1, M2")
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.code

class Filiere(models.Model):
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=255)
    a_des_specialites = models.BooleanField(default=False)
    specialite_unique_auto = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='specialites')
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=255)

    class Meta:
        unique_together = ('filiere', 'code')

    def __str__(self):
        return f"{self.filiere.code} - {self.nom}"

class Semestre(models.Model):
    code = models.CharField(max_length=10, help_text="Ex: S1, S2")
    nom = models.CharField(max_length=50)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='semestres')

    class Meta:
        unique_together = ('code', 'niveau')

    def __str__(self):
        return f"{self.niveau.code} - {self.code}"

class UE(models.Model):
    code = models.CharField(max_length=20)
    intitule = models.CharField(max_length=255)
    credits = models.DecimalField(max_digits=4, decimal_places=1)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='ues')
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, blank=True, related_name='ues')

    class Meta:
        unique_together = ('code', 'semestre')

    def __str__(self):
        return f"{self.code} - {self.intitule}"

class EC(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='ecs')
    code = models.CharField(max_length=20)
    intitule = models.CharField(max_length=255)
    coefficient = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('ue', 'code')

    def __str__(self):
        return f"{self.code} - {self.intitule}"
