from django.db import models
from apps.accounts.models import UtilisateurAdmin


class ImportFichier(models.Model):
    STATUT_CHOICES = (
        ("EN_ATTENTE", "En attente"),
        ("EN_COURS", "En cours"),
        ("TERMINE", "Terminé"),
        ("ERREUR", "Erreur"),
    )
    fichier = models.FileField(upload_to="imports/")
    date_upload = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(UtilisateurAdmin, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="EN_ATTENTE"
    )
    rapport = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Import {self.id} du {self.date_upload.strftime('%Y-%m-%d %H:%M')}"


class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(
        ImportFichier, on_delete=models.CASCADE, related_name="lignes"
    )
    numero_ligne = models.PositiveIntegerField()
    donnees_json = models.JSONField()
    statut = models.CharField(max_length=20, default="EN_ATTENTE")
    erreurs = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Ligne {self.numero_ligne} (Import {self.import_fichier_id})"


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    mapping_json = models.JSONField(help_text="Format: {'colonne_excel': 'champ_db'}")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
