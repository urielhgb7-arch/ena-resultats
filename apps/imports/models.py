from django.db import models
from django.conf import settings

class MappingTemplate(models.Model):
    nom = models.CharField(max_length=150)
    config_colonnes = models.JSONField()

    class Meta:
        db_table = 'mapping_template'

    def __str__(self):
        return self.nom

class ImportFichier(models.Model):
    nom_fichier = models.CharField(max_length=300)
    date_import = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    mapping = models.ForeignKey(MappingTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(max_length=20, default='en_attente')

    class Meta:
        db_table = 'import_fichier'

    def __str__(self):
        return self.nom_fichier

class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, db_column='import_id')
    numero_ligne = models.IntegerField()
    donnees_brutes = models.JSONField()
    statut_traitement = models.CharField(max_length=20, default='en_attente')

    class Meta:
        db_table = 'ligne_brute'

    def __str__(self):
        return f"Ligne {self.numero_ligne} - {self.import_fichier}"
