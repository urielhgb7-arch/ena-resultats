from django.db import models
from apps.filieres.models import AnneeAcademique, Semestre, Filiere, Specialite

class SessionResultat(models.Model):
    TYPES_SESSION = [
        ('normale', 'Normale'),
        ('rattrapage', 'Rattrapage'),
        ('ajournement', 'Ajournement'),
    ]
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    type_session = models.CharField(max_length=20, choices=TYPES_SESSION, default='normale')

    def __str__(self):
        return f"{self.semestre} - {self.annee_academique} ({self.get_type_session_display()})"

class UE(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    credits = models.PositiveIntegerField(default=1)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='ues')

    def __str__(self):
        return f"{self.code} - {self.nom}"

class EC(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='ecs')
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    coefficient = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.code} - {self.nom} (Coef: {self.coefficient})"

class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"

class NoteEC(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes_ec')
    ec = models.ForeignKey(EC, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE)
    note = models.FloatField()

    class Meta:
        unique_together = ('etudiant', 'ec', 'session')

    def __str__(self):
        return f"{self.etudiant} - {self.ec.code}: {self.note}"

class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='resultats_ue')
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE)
    moyenne_ue = models.FloatField(help_text="Strictement figé à l'import, ne pas recalculer dynamiquement.")
    valide = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'ue', 'session')

    def __str__(self):
        return f"{self.etudiant} - {self.ue.code}: {self.moyenne_ue} (Valide: {self.valide})"
