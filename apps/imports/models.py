from django.db import models


class ImportFichier(models.Model):
    fichier = models.CharField(max_length=255)
    date_import = models.DateTimeField(auto_now_add=True)


class LigneBrute(models.Model):
    import_fichier = models.ForeignKey(ImportFichier, on_delete=models.CASCADE)
    donnees = models.JSONField()


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    mapping = models.JSONField()
