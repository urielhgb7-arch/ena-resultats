from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.filieres.models import AnneeAcademique, Semestre, Filiere, Specialite

class SessionResultat(models.Model):
    class TypeSession(models.TextChoices):
        NORMALE = 'NORMALE', _('Normale')
        RATTRAPAGE = 'RATTRAPAGE', _('Rattrapage')

    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name='sessions')
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='sessions')
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='sessions')
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, null=True, blank=True, related_name='sessions')
    type_session = models.CharField(max_length=20, choices=TypeSession.choices)
    est_publiee = models.BooleanField(default=False)
    date_publication = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Session de résultat')
        verbose_name_plural = _('Sessions de résultats')
        unique_together = ('annee_academique', 'semestre', 'filiere', 'specialite', 'type_session')

    def __str__(self):
        spec_str = f" - {self.specialite.code}" if self.specialite else ""
        return f"{self.annee_academique} - {self.filiere.code}{spec_str} - {self.semestre} - {self.get_type_session_display()}"

class UE(models.Model):
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    credits = models.PositiveIntegerField()
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='ues')

    class Meta:
        verbose_name = _('Unité d\'Enseignement (UE)')
        verbose_name_plural = _('Unités d\'Enseignement (UE)')
        unique_together = ('session', 'code')

    def __str__(self):
        return f"{self.code} - {self.libelle} ({self.credits} crédits)"

class EC(models.Model):
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='ecs')

    class Meta:
        verbose_name = _('Élément Constitutif (EC)')
        verbose_name_plural = _('Éléments Constitutifs (EC)')
        unique_together = ('ue', 'code')

    def __str__(self):
        return f"{self.code} - {self.libelle}"

class Etudiant(models.Model):
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _('Étudiant')
        verbose_name_plural = _('Étudiants')

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"

class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='resultats_ue')
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='resultats')
    # Moyenne UE is strictly imported and NEVER calculated dynamically.
    moyenne_ue = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = _('Résultat UE')
        verbose_name_plural = _('Résultats UE')
        unique_together = ('etudiant', 'ue')

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code} : {self.moyenne_ue}"

class NoteEC(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes_ec')
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name='notes')
    note = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = _('Note EC')
        verbose_name_plural = _('Notes EC')
        unique_together = ('etudiant', 'ec')

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ec.code} : {self.note}"
