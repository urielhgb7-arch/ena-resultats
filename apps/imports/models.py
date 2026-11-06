from django.db import models
from apps.filieres.models import Filiere, Niveau
from apps.resultats.models import SessionResultat
from django.conf import settings


class ImportFichier(models.Model):
    STATUT_CHOICES = (
        ("en_attente", "En attente"),
        ("en_cours", "En cours"),
        ("termine", "Terminé"),
        ("erreur", "Erreur"),
    )

    fichier = models.FileField(upload_to="imports/%Y/%m/%d/")
    date_upload = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="en_attente"
    )
    session = models.ForeignKey(
        SessionResultat,
        on_delete=models.CASCADE,
        related_name="imports",
        null=True,
        blank=True,
    )
    filiere = models.ForeignKey(
        Filiere, on_delete=models.SET_NULL, null=True, blank=True
    )
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True)
    erreurs_log = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Import {self.id} du {self.date_upload.strftime('%Y-%m-%d %H:%M')}"


class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(
        ImportFichier, on_delete=models.CASCADE, related_name="lignes"
    )
    numero_ligne = models.PositiveIntegerField()
    donnees = models.JSONField(help_text="Données brutes de la ligne Excel")
    est_valide = models.BooleanField(default=False)
    erreurs = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["numero_ligne"]

    def __str__(self):
        return f"Ligne {self.numero_ligne} de l'import {self.import_fichier.id}"


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    mapping = models.JSONField(
        help_text="Dictionnaire associant colonnes attendues et colonnes du fichier"
    )

    def __str__(self):
        return self.nom
