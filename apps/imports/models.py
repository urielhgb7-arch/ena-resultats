from django.db import models

from apps.resultats.models import SessionResultat
from django.conf import settings

class ImportFichier(models.Model):
    STATUTS_IMPORT = [
        ('U', 'Uploadé'),
        ('M', 'Mappé'),
        ('V', 'Validé'),
        ('P', 'Publié'),
        ('E', 'Erreur'),
    ]
    fichier = models.FileField(upload_to='imports/')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_upload = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=1, choices=STATUTS_IMPORT, default='U')
    session_cible = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, null=True, blank=True)
    logs_erreur = models.TextField(blank=True)

    def __str__(self):
        return f"Import {self.id} - {self.get_statut_display()}"


class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, related_name='lignes')
    numero_ligne = models.PositiveIntegerField()
    donnees_json = models.JSONField()
    est_valide = models.BooleanField(default=False)
    erreurs_validation = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['numero_ligne']

    def __str__(self):
        return f"Ligne {self.numero_ligne} de l'import {self.import_fichier.id}"


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    mapping_json = models.JSONField(help_text="Dictionnaire associant colonnes Excel et champs attendus")

    def __str__(self):
        return self.nom
