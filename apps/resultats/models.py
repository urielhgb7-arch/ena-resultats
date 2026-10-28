from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.filieres.models import AnneeAcademique, Semestre, Filiere, Specialite
from django.conf import settings

class SessionResultat(models.Model):
    class TypeSession(models.TextChoices):
        NORMALE = 'normale', _('Normale')
        RATTRAPAGE = 'rattrapage', _('Rattrapage')
        AJOURNEMENT = 'ajournement', _('Ajournement')

    class Statut(models.TextChoices):
        BROUILLON = 'brouillon', _('Brouillon')
        EN_ATTENTE = 'en_attente', _('En attente de validation')
        VALIDE = 'valide', _('Validé')
        PUBLIE = 'publie', _('Publié')

    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name="sessions")
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="sessions")
    type_session = models.CharField(max_length=20, choices=TypeSession.choices, default=TypeSession.NORMALE)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.BROUILLON)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="sessions")
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, related_name="sessions", null=True, blank=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="sessions_creees")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_publication = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Session de Résultat")
        verbose_name_plural = _("Sessions de Résultats")
        unique_together = ('annee_academique', 'semestre', 'type_session', 'filiere', 'specialite')
        db_table = 'resultats_sessionresultat'

    def __str__(self):
        return f"{self.filiere.code} - S{self.semestre.numero} ({self.get_type_session_display()}) - {self.annee_academique.libelle}"

class UE(models.Model):
    code = models.CharField(max_length=50)
    intitule = models.CharField(max_length=255)
    credits = models.IntegerField()
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name="ues")

    class Meta:
        verbose_name = _("Unité d'Enseignement (UE)")
        verbose_name_plural = _("Unités d'Enseignement (UE)")
        unique_together = ('code', 'session')
        db_table = 'resultats_ue'

    def __str__(self):
        return f"{self.code} - {self.intitule}"

class EC(models.Model):
    code = models.CharField(max_length=50)
    intitule = models.CharField(max_length=255)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="ecs")

    class Meta:
        verbose_name = _("Élément Constitutif (EC)")
        verbose_name_plural = _("Éléments Constitutifs (EC)")
        unique_together = ('code', 'ue')
        db_table = 'resultats_ec'

    def __str__(self):
        return f"{self.code} - {self.intitule}"

class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Étudiant")
        verbose_name_plural = _("Étudiants")
        db_table = 'resultats_etudiant'

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"

class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="resultats_ue")
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="resultats")
    moyenne_ue = models.DecimalField(max_digits=5, decimal_places=2, help_text="Valeur figée depuis l'import, ne doit pas être recalculée")
    valide = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Résultat UE")
        verbose_name_plural = _("Résultats UE")
        unique_together = ('etudiant', 'ue')
        db_table = 'resultats_resultatue'

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code} : {self.moyenne_ue}"

class NoteEC(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="notes_ec")
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name="notes")
    valeur = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Note EC")
        verbose_name_plural = _("Notes EC")
        unique_together = ('etudiant', 'ec')
        db_table = 'resultats_noteec'

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ec.code} : {self.valeur}"
