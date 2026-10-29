from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class ImportFichier(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = 'EN_ATTENTE', _('En attente de traitement')
        EN_COURS = 'EN_COURS', _('En cours de traitement')
        TERMINE = 'TERMINE', _('Terminé')
        ERREUR = 'ERREUR', _('Erreur')

    fichier = models.FileField(upload_to='imports/')
    date_import = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Import {self.id} - {self.get_statut_display()} le {self.date_import}"

    class Meta:
        verbose_name = _('Import de Fichier')
        verbose_name_plural = _('Imports de Fichiers')

class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, related_name='lignes')
    donnees = models.JSONField()

    def __str__(self):
        return f"Ligne de l'import {self.import_fichier_id}"

    class Meta:
        verbose_name = _('Ligne Brute')
        verbose_name_plural = _('Lignes Brutes')

class MappingTemplate(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    configuration = models.JSONField()

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = _('Template de Mapping')
        verbose_name_plural = _('Templates de Mapping')
