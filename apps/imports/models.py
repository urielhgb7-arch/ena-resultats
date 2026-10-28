from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.resultats.models import SessionResultat
from django.conf import settings

class ImportFichier(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = 'en_attente', _('En attente de traitement')
        EN_COURS = 'en_cours', _('En cours de traitement')
        TERMINE = 'termine', _('Terminé avec succès')
        ERREUR = 'erreur', _('Erreur lors du traitement')

    fichier = models.FileField(upload_to='imports/')
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name="imports")
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="imports_crees")
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE)
    date_import = models.DateTimeField(auto_now_add=True)
    rapport_erreur = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Import de fichier")
        verbose_name_plural = _("Imports de fichiers")
        db_table = 'imports_importfichier'

    def __str__(self):
        return f"Import {self.id} - {self.session} ({self.get_statut_display()})"

class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, related_name="lignes")
    numero_ligne = models.IntegerField()
    donnees = models.JSONField(help_text="Données brutes de la ligne Excel")
    est_valide = models.BooleanField(default=False)
    erreurs = models.JSONField(blank=True, null=True, help_text="Liste des erreurs de validation")

    class Meta:
        verbose_name = _("Ligne brute")
        verbose_name_plural = _("Lignes brutes")
        ordering = ['numero_ligne']
        db_table = 'imports_lignebrute'

    def __str__(self):
        return f"Ligne {self.numero_ligne} (Import {self.import_fichier_id})"

class MappingTemplate(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    mapping = models.JSONField(help_text="Dictionnaire associant les colonnes attendues aux colonnes du fichier Excel")

    class Meta:
        verbose_name = _("Template de mapping")
        verbose_name_plural = _("Templates de mapping")
        db_table = 'imports_mappingtemplate'

    def __str__(self):
        return self.nom
