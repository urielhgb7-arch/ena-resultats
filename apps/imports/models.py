from django.db import models
from django.conf import settings
from apps.resultats.models import SessionResultat


class ImportFichier(models.Model):
    STATUT_CHOICES = (
        ("EN_ATTENTE", "En attente"),
        ("EN_COURS", "En cours"),
        ("TERMINE", "Terminé"),
        ("ERREUR", "Erreur"),
    )
    fichier = models.FileField(upload_to="imports/")
    date_import = models.DateTimeField(auto_now_add=True)
    importateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="EN_ATTENTE"
    )
    session = models.ForeignKey(
        SessionResultat, on_delete=models.CASCADE, related_name="imports"
    )

    def __str__(self):
        return f"Import {self.id} - {self.date_import}"


class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(
        ImportFichier, on_delete=models.CASCADE, related_name="lignes"
    )
    donnees_json = models.JSONField()
    validee = models.BooleanField(default=False)
    erreurs = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Ligne {self.id} de l'import {self.import_fichier.id}"


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=100)
    mapping_json = models.JSONField(help_text="Format: {'colonne_excel': 'champ_bd'}")

    def __str__(self):
        return self.nom
