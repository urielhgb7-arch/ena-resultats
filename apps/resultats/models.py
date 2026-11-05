from django.db import models
from apps.filieres.models import AnneeAcademique, Semestre, UE, EC, Filiere, Specialite, Niveau

class SessionResultat(models.Model):
    TYPES_SESSION = [
        ('normale', 'Normale'),
        ('rattrapage', 'Rattrapage')
    ]
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    type_session = models.CharField(max_length=20, choices=TYPES_SESSION)
    est_publie = models.BooleanField(default=False)
    date_publication = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('annee_academique', 'semestre', 'type_session')

    def __str__(self):
        return f"{self.annee_academique} - {self.semestre} - {self.get_type_session_display()}"

class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenoms}"

class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='resultats_ue')
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='resultats')
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='resultats_ue')

    # Règle non négociable: moyenne_ue est figée, jamais recalculée
    moyenne_ue = models.DecimalField(max_digits=5, decimal_places=2)
    est_validee = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'ue', 'session')

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code}: {self.moyenne_ue}"

class NoteEC(models.Model):
    resultat_ue = models.ForeignKey(ResultatUE, on_delete=models.CASCADE, related_name='notes_ec')
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name='notes')
    note = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('resultat_ue', 'ec')

    def __str__(self):
        return f"{self.resultat_ue.etudiant.matricule} - {self.ec.code}: {self.note}"
