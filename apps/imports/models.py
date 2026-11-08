from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.resultats.models import SessionResultat

User = get_user_model()

class ImportFichier(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = 'EN_ATTENTE', _('En attente')
        EN_COURS = 'EN_COURS', _('En cours')
        TERMINE = 'TERMINE', _('Terminé')
        ERREUR = 'ERREUR', _('Erreur')

    fichier = models.FileField(upload_to='imports_bruts/')
    date_upload = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE)
    message_erreur = models.TextField(blank=True, null=True)
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE, related_name='imports', null=True, blank=True)

    class Meta:
        verbose_name = _('Import de fichier')
        verbose_name_plural = _('Imports de fichiers')

    def __str__(self):
        return f"Import {self.id} - {self.get_statut_display()} - {self.date_upload.strftime('%Y-%m-%d %H:%M')}"

class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE, related_name='lignes')
    numero_ligne = models.PositiveIntegerField()
    donnees = models.JSONField(help_text=_('Contenu brut de la ligne (JSON)'))

    class Meta:
        verbose_name = _('Ligne brute')
        verbose_name_plural = _('Lignes brutes')
        ordering = ['numero_ligne']

    def __str__(self):
        return f"Ligne {self.numero_ligne} de l'import {self.import_fichier.id}"

class MappingTemplate(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    mapping = models.JSONField(help_text=_('Mapping des colonnes Excel vers les champs du modèle (JSON)'))

    class Meta:
        verbose_name = _('Template de mapping')
        verbose_name_plural = _('Templates de mapping')

    def __str__(self):
        return self.nom
