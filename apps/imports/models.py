from django.db import models


class MappingTemplate(models.Model):
    nom = models.CharField(max_length=150)
    config_colonnes = models.JSONField()

    class Meta:
        db_table = "mapping_template"

    def __str__(self):
        return self.nom


class ImportFichier(models.Model):
    class StatutImport(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        VALIDE = "valide", "Validé"
        APPLIQUE = "applique", "Appliqué"
        ANNULE = "annule", "Annulé"

    nom_fichier = models.CharField(max_length=300)
    date_import = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(
        "accounts.UtilisateurAdmin", on_delete=models.SET_NULL, null=True, blank=True
    )
    mapping = models.ForeignKey(
        MappingTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    statut = models.CharField(
        max_length=20, choices=StatutImport.choices, default=StatutImport.EN_ATTENTE
    )

    class Meta:
        db_table = "import_fichier"

    def __str__(self):
        return self.nom_fichier


class LigneBrute(models.Model):
    class StatutTraitement(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"

    import_fichier = models.ForeignKey(
        ImportFichier, on_delete=models.CASCADE, db_column="import_id"
    )
    numero_ligne = models.IntegerField()
    donnees_brutes = models.JSONField()
    statut_traitement = models.CharField(
        max_length=20,
        choices=StatutTraitement.choices,
        default=StatutTraitement.EN_ATTENTE,
    )

    class Meta:
        db_table = "ligne_brute"
