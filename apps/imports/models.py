from django.db import models
from apps.resultats.models import SessionResultat
from django.core.validators import FileExtensionValidator
from django.conf import settings

class ImportFichier(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('termine', 'Terminé'),
        ('erreur', 'Erreur')
    ]
    fichier = models.FileField(
        upload_to='imports/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx'])]
    )
    date_import = models.DateTimeField(auto_now_add=True)
    importateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    session_cible = models.ForeignKey(SessionResultat, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    rapport_erreurs = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Import {self.id} du {self.date_import.strftime('%d/%m/%Y %H:%M')} par {self.importateur}"

class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, related_name='lignes')
    numero_ligne = models.IntegerField()
    donnees_json = models.JSONField()
    est_valide = models.BooleanField(default=False)
    erreurs_validation = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['numero_ligne']

    def __str__(self):
        return f"Ligne {self.numero_ligne} de l'import {self.import_fichier.id}"

class MappingTemplate(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    mapping_json = models.JSONField(help_text="Format: {'colonne_excel': 'champ_bd'}")

    def __str__(self):
        return self.nom
