from django.db import models
from apps.filieres.models import AnneeAcademique, Semestre
from apps.accounts.models import UtilisateurAdmin

class ImportFichier(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('erreur', 'Erreur'),
    ]
    fichier = models.FileField(upload_to='imports/')
    date_import = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    importe_par = models.ForeignKey(UtilisateurAdmin, on_delete=models.CASCADE)

    def __str__(self):
        return f"Import {self.id} du {self.date_import.strftime('%d/%m/%Y')} - {self.get_statut_display()}"

class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, related_name='lignes')
    donnees_json = models.JSONField()
    statut_validation = models.CharField(max_length=50, default='non_valide')
    erreurs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Ligne {self.id} (Import {self.import_fichier_id})"

class MappingTemplate(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    mapping_json = models.JSONField()
    cree_par = models.ForeignKey(UtilisateurAdmin, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom
