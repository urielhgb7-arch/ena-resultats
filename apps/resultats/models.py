from django.db import models
from apps.filieres.models import AnneeAcademique, Semestre, UE, EC, Filiere

class SessionResultat(models.Model):
    TYPES_SESSION = (
        ('NORMALE', 'Session Normale'),
        ('RATTRAPAGE', 'Session de Rattrapage'),
    )

    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name='sessions')
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='sessions')
    type_session = models.CharField(max_length=20, choices=TYPES_SESSION)

    class Meta:
        unique_together = ('annee_academique', 'semestre', 'type_session')

    def __str__(self):
        return f"{self.type_session} - {self.semestre} ({self.annee_academique})"

class Etudiant(models.Model):
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"

class NoteEC(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name='notes')
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='notes')
    valeur = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    est_absent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'ec', 'session')

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ec.code} - {self.valeur}"

class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='resultats_ue')
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='resultats')
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='resultats_ue')

    # "ResultatUE.moyenne_ue est figée au moment de l'import, jamais recalculée"
    moyenne_ue = models.DecimalField(max_digits=4, decimal_places=2)
    est_validee = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'ue', 'session')

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code} - {self.moyenne_ue}"
