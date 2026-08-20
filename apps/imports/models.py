from simple_history.models import HistoricalRecords
from django.db import models
from django.conf import settings


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=150)
    # ex: {"matricule_col": 2, "blocs_ue": [{"ue_code": "MTH1121",
    #      "ec_cols": [{"code":"EC1","col":4}], "moy_col": 5, "statut_col": 6}, ...]}
    config_colonnes = models.JSONField()

    def __str__(self):
        return self.nom


class ImportFichier(models.Model):
    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("valide", "Validé"),
        ("applique", "Appliqué"),
        ("annule", "Annulé"),
    ]
    nom_fichier = models.CharField(max_length=300)
    fichier = models.FileField(upload_to="imports_bruts/")
    date_import = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    mapping = models.ForeignKey(
        MappingTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="en_attente"
    )
    history = HistoricalRecords()


    class Meta:
        ordering = ["-date_import"]

    def __str__(self):
        return f"{self.nom_fichier} ({self.get_statut_display()})"


class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(
        ImportFichier, on_delete=models.CASCADE, related_name="lignes"
    )
    numero_ligne = models.PositiveIntegerField()
    donnees_brutes = models.JSONField()          # ligne Excel telle quelle
    statut_traitement = models.CharField(max_length=20, default="en_attente")

    class Meta:
        ordering = ["numero_ligne"]

    def __str__(self):
        return f"Ligne {self.numero_ligne} - {self.import_fichier}"
