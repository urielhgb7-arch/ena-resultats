from django.db import models
from apps.core.models import SessionResultat
from django.conf import settings


class ImportFichier(models.Model):
    class StatutImport(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente de mapping"
        MAPPING_VALIDE = "MAPPING_VALIDE", "Mapping validé"
        TRAITEMENT = "TRAITEMENT", "En cours de traitement"
        TERMINE = "TERMINE", "Terminé avec succès"
        ERREUR = "ERREUR", "Erreur"

    fichier = models.FileField(upload_to="imports/%Y/%m/%d/")
    session = models.ForeignKey(
        SessionResultat, on_delete=models.CASCADE, related_name="imports"
    )
    statut = models.CharField(
        max_length=20, choices=StatutImport.choices, default=StatutImport.EN_ATTENTE
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="imports_crees",
    )

    class Meta:
        verbose_name = "Fichier d'import"
        verbose_name_plural = "Fichiers d'import"
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Import {self.id} - {self.session} ({self.get_statut_display()})"


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    mapping_json = models.JSONField(
        help_text="Dictionnaire associant les champs de la base de données aux colonnes du fichier Excel"
    )

    class Meta:
        verbose_name = "Modèle de mapping"
        verbose_name_plural = "Modèles de mapping"

    def __str__(self):
        return self.nom


class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(
        ImportFichier, on_delete=models.CASCADE, related_name="lignes_brutes"
    )
    numero_ligne = models.PositiveIntegerField()
    donnees_json = models.JSONField()
    est_valide = models.BooleanField(default=False)
    erreurs = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Ligne brute"
        verbose_name_plural = "Lignes brutes"
        ordering = ["import_fichier", "numero_ligne"]
        unique_together = ("import_fichier", "numero_ligne")

    def __str__(self):
        return f"Ligne {self.numero_ligne} (Import {self.import_fichier.id})"
