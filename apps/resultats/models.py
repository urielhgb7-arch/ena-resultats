from django.db import models
from apps.filieres.models import SessionResultat


class UE(models.Model):
    STATUT_CHOICES = [
        ("brouillon", "Brouillon"),
        ("publie", "Publié"),
    ]
    session = models.ForeignKey(
        SessionResultat, on_delete=models.CASCADE, related_name="ues"
    )
    code = models.CharField(max_length=30)                # ex: MTH1121
    nom = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()
    fichier_pdf_archive = models.FileField(
        upload_to="pv_archives/", null=True, blank=True
    )
    date_publication = models.DateField(null=True, blank=True)
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="brouillon"
    )

    class Meta:
        verbose_name = "UE"
        verbose_name_plural = "UE"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.nom}"


class EC(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="ecs")
    code = models.CharField(max_length=10)                 # EC1, EC2
    nom = models.CharField(max_length=200)

    class Meta:
        verbose_name = "EC"
        verbose_name_plural = "EC"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Etudiant(models.Model):
    matricule = models.CharField(max_length=30, unique=True, null=True, blank=True)
    annee_promo = models.CharField(max_length=10, blank=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)

    class Meta:
        ordering = ["nom", "prenom"]
        indexes = [
            models.Index(fields=["nom", "prenom"]),
        ]

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class NoteEC(models.Model):
    etudiant = models.ForeignKey(
        Etudiant, on_delete=models.CASCADE, related_name="notes_ec"
    )
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name="notes")
    import_fichier = models.ForeignKey(
        "imports.ImportFichier", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="notes_ec",
    )
    note = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ("etudiant", "ec")
        verbose_name = "Note EC"
        verbose_name_plural = "Notes EC"

    def __str__(self):
        return f"{self.etudiant} - {self.ec} : {self.note}"


class ResultatUE(models.Model):
    STATUT_CHOICES = [
        ("V", "Validé"),
        ("NV", "Non validé"),
        ("V*", "Validé*"),
    ]
    etudiant = models.ForeignKey(
        Etudiant, on_delete=models.CASCADE, related_name="resultats_ue"
    )
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="resultats")
    import_fichier = models.ForeignKey(
        "imports.ImportFichier", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="resultats_ue",
    )
    # Moyenne figée au moment de l'import/saisie - ne JAMAIS recalculer
    # dynamiquement depuis NoteEC, ce chiffre correspond au PV officiel signé.
    moyenne_ue = models.DecimalField(max_digits=4, decimal_places=2)
    statut = models.CharField(max_length=5, choices=STATUT_CHOICES)

    class Meta:
        unique_together = ("etudiant", "ue")
        verbose_name = "Résultat UE"
        verbose_name_plural = "Résultats UE"

    def __str__(self):
        return f"{self.etudiant} - {self.ue} : {self.moyenne_ue} ({self.statut})"
