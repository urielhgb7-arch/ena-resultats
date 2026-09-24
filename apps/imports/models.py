from django.db import models
from apps.accounts.models import UtilisateurAdmin


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=150)
    config_colonnes = models.JSONField()

    class Meta:
        db_table = 'mapping_template'

    def __str__(self):
        return self.nom


class ImportFichier(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('applique', 'Appliqué'),
        ('annule', 'Annulé'),
    ]
    nom_fichier = models.CharField(max_length=300)
    date_import = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(UtilisateurAdmin, on_delete=models.SET_NULL, null=True, blank=True)
    mapping = models.ForeignKey(MappingTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        db_table = 'import_fichier'

    def __str__(self):
        return f"Import {self.nom_fichier} le {self.date_import}"


class LigneBrute(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        # Add other statuses as needed
    ]
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, db_column='import_id')
    numero_ligne = models.IntegerField()
    donnees_brutes = models.JSONField()
    statut_traitement = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        db_table = 'ligne_brute'

    def __str__(self):
        return f"Ligne {self.numero_ligne} de l'import {self.import_fichier_id}"
