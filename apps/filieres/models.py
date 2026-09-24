from django.db import models
from apps.core.models import Niveau


class Filiere(models.Model):
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    a_des_specialites = models.BooleanField(default=True)
    specialite_unique_auto = models.BooleanField(default=False)

    class Meta:
        db_table = 'filiere'

    def __str__(self):
        return f"{self.nom} - {self.niveau}"


class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)

    class Meta:
        db_table = 'specialite'

    def __str__(self):
        return f"{self.nom} ({self.filiere.nom})"


class Semestre(models.Model):
    TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('stage', 'Stage'),
    ]
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=20)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='normal')

    class Meta:
        db_table = 'semestre'

    def __str__(self):
        return f"{self.libelle} - {self.filiere.nom}"


class SessionResultat(models.Model):
    TYPE_CHOICES = [
        ('normale', 'Normale'),
        ('rattrapage', 'Rattrapage'),
        ('ajournement', 'Ajournement'),
        ('re_enjambement', 'Ré-enjambement'),
    ]
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)

    class Meta:
        db_table = 'session_resultat'

    def __str__(self):
        return f"Session {self.type} - {self.semestre}"


class UE(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE)
    code = models.CharField(max_length=30)
    nom = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()
    fichier_pdf_archive = models.CharField(max_length=300, null=True, blank=True)
    date_publication = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')

    class Meta:
        db_table = 'ue'
        indexes = [
            models.Index(fields=['session']),
        ]

    def __str__(self):
        return f"{self.code} - {self.nom}"


class EC(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=200)

    class Meta:
        db_table = 'ec'

    def __str__(self):
        return f"{self.code} - {self.nom}"
