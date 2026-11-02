from django.db import models
from django.conf import settings
from apps.resultats.models import SessionResultat

class MappingTemplate(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    mapping_colonnes = models.JSONField(help_text="Format JSON pour mapper les en-têtes Excel aux champs du système")

    def __str__(self):
        return self.nom

class ImportFichier(models.Model):
    STATUTS = (
        ('BROUILLON', 'Brouillon'),
        ('EN_ATTENTE', 'En attente de validation'),
        ('VALIDE', 'Validé'),
        ('REJETE', 'Rejeté'),
    )

    fichier = models.FileField(upload_to='imports/%Y/%m/%d/')
    statut = models.CharField(max_length=20, choices=STATUTS, default='BROUILLON')
    date_import = models.DateTimeField(auto_now_add=True)
    importe_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='imports')
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='imports')
    mapping = models.ForeignKey(MappingTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Import {self.id} - {self.statut} - {self.date_import}"

class LigneBrute(models.Model):
    STATUTS_LIGNE = (
        ('VALIDE', 'Valide'),
        ('ERREUR', 'Erreur'),
        ('IGNORE', 'Ignoré'),
    )

    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, related_name='lignes')
    numero_ligne = models.PositiveIntegerField()
    donnees = models.JSONField(help_text="Données brutes extraites de la ligne Excel")
    statut = models.CharField(max_length=20, choices=STATUTS_LIGNE, default='VALIDE')
    erreurs = models.JSONField(null=True, blank=True, help_text="Liste des erreurs de validation pour cette ligne")

    class Meta:
        ordering = ['numero_ligne']

    def __str__(self):
        return f"Ligne {self.numero_ligne} (Import {self.import_fichier_id})"
