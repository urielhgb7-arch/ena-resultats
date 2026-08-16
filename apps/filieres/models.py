from django.db import models


class AnneeAcademique(models.Model):
    libelle = models.CharField(max_length=20)          # ex: "2025-2026"
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-libelle"]
        verbose_name = "Année académique"
        verbose_name_plural = "Années académiques"

    def __str__(self):
        return self.libelle


class Niveau(models.Model):
    annee = models.ForeignKey(
        AnneeAcademique, on_delete=models.CASCADE, related_name="niveaux"
    )
    libelle = models.CharField(max_length=10)           # L1, L2, L3

    class Meta:
        ordering = ["libelle"]

    def __str__(self):
        return f"{self.libelle} ({self.annee})"


class Filiere(models.Model):
    niveau = models.ForeignKey(
        Niveau, on_delete=models.CASCADE, related_name="filieres"
    )
    nom = models.CharField(max_length=150)
    # --- flags d'exception : pilotables par la donnée, jamais codés en dur ---
    a_des_specialites = models.BooleanField(default=True)
    specialite_unique_auto = models.BooleanField(default=False)

    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Filières"

    def __str__(self):
        return self.nom

    @property
    def specialite_par_defaut(self):
        """Retourne la spécialité unique si specialite_unique_auto est actif."""
        if self.specialite_unique_auto:
            return self.specialites.first()
        return None


class Specialite(models.Model):
    filiere = models.ForeignKey(
        Filiere, on_delete=models.CASCADE, related_name="specialites"
    )
    nom = models.CharField(max_length=150)

    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Spécialités"

    def __str__(self):
        return self.nom


class Semestre(models.Model):
    TYPE_CHOICES = [
        ("normal", "Normal"),
        ("stage", "Stage"),
    ]
    filiere = models.ForeignKey(
        Filiere, on_delete=models.CASCADE, related_name="semestres"
    )
    libelle = models.CharField(max_length=20)            # "Semestre 1"...
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="normal")

    class Meta:
        ordering = ["libelle"]

    def __str__(self):
        return f"{self.libelle} - {self.filiere}"


class SessionResultat(models.Model):
    TYPE_CHOICES = [
        ("normale", "Session normale"),
        ("rattrapage", "Rattrapage"),
        ("ajournement", "Ajournement"),
        ("re_enjambement", "Ré-enjambement"),
    ]
    semestre = models.ForeignKey(
        Semestre, on_delete=models.CASCADE, related_name="sessions"
    )
    specialite = models.ForeignKey(
        Specialite, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="sessions",
    )  # NULL si tronc commun (ex: Secrétariat de Gestion)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Session de résultats"
        verbose_name_plural = "Sessions de résultats"

    def __str__(self):
        return f"{self.get_type_display()} - {self.semestre}"
