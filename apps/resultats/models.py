from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.filieres.models import AnneeAcademique, Semestre, UE, EC

class SessionResultat(models.Model):
    class TypeSession(models.TextChoices):
        NORMALE = 'NORMALE', _('Normale')
        RATTRAPAGE = 'RATTRAPAGE', _('Rattrapage')

    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name='sessions')
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='sessions')
    type_session = models.CharField(max_length=20, choices=TypeSession.choices, default=TypeSession.NORMALE)

    def __str__(self):
        return f"{self.semestre} - {self.annee_academique} ({self.get_type_session_display()})"

    class Meta:
        verbose_name = _('Session de Résultat')
        verbose_name_plural = _('Sessions de Résultat')
        unique_together = ('annee_academique', 'semestre', 'type_session')

class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"

    class Meta:
        verbose_name = _('Étudiant')
        verbose_name_plural = _('Étudiants')

class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='resultats_ue')
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='resultats')
    session_resultat = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='resultats_ue')
    moyenne_ue = models.DecimalField(max_digits=5, decimal_places=2, help_text="Moyenne figée au moment de l'import, jamais recalculée")

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code} : {self.moyenne_ue}"

    class Meta:
        verbose_name = _('Résultat UE')
        verbose_name_plural = _('Résultats UE')
        unique_together = ('etudiant', 'ue', 'session_resultat')

class NoteEC(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes_ec')
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name='notes')
    session_resultat = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='notes_ec')
    note = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ec.code} : {self.note}"

    class Meta:
        verbose_name = _('Note EC')
        verbose_name_plural = _('Notes EC')
        unique_together = ('etudiant', 'ec', 'session_resultat')
