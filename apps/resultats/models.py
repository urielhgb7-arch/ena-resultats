from django.db import models
from apps.filieres.models import AnneeAcademique, Semestre, Filiere, Specialite, UE, EC, Etudiant

class SessionResultat(models.Model):
    TYPES_SESSION = [
        ('N', 'Normale'),
        ('R', 'Rattrapage'),
        ('S', 'Speciale'),
    ]
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, null=True, blank=True)
    type_session = models.CharField(max_length=1, choices=TYPES_SESSION, default='N')
    est_publie = models.BooleanField(default=False)
    date_publication = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('annee_academique', 'semestre', 'filiere', 'specialite', 'type_session')

    def __str__(self):
        return f"{self.filiere.code} - {self.semestre.nom} - {self.annee_academique.annee} ({self.get_type_session_display()})"


class ResultatUE(models.Model):
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='resultats_ue')
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='resultats_ue')
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    moyenne_ue = models.FloatField(help_text="Moyenne figée de l'UE, non recalculable")
    valide = models.BooleanField(default=False)

    class Meta:
        unique_together = ('session', 'etudiant', 'ue')

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code} : {self.moyenne_ue}"


class NoteEC(models.Model):
    resultat_ue = models.ForeignKey(ResultatUE, on_delete=models.CASCADE, related_name='notes_ec')
    ec = models.ForeignKey(EC, on_delete=models.CASCADE)
    note = models.FloatField()

    class Meta:
        unique_together = ('resultat_ue', 'ec')

    def __str__(self):
        return f"{self.ec.code} - {self.note}"
