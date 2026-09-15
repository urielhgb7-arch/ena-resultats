from django.db import models
from apps.filieres.models import UE, EC, Specialite, Filiere
from apps.core.models import SessionResultat


class Etudiant(models.Model):
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)
    filiere = models.ForeignKey(
        Filiere, on_delete=models.CASCADE, related_name="etudiants"
    )
    specialite = models.ForeignKey(
        Specialite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="etudiants",
    )

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ["nom", "prenoms"]

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenoms}"


class ResultatUE(models.Model):
    etudiant = models.ForeignKey(
        Etudiant, on_delete=models.CASCADE, related_name="resultats_ue"
    )
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="resultats")
    session = models.ForeignKey(
        SessionResultat, on_delete=models.CASCADE, related_name="resultats_ue"
    )
    moyenne_ue = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Moyenne figée lors de l'import, non recalculée dynamiquement.",
    )
    est_valide = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Résultat UE"
        verbose_name_plural = "Résultats UE"
        unique_together = ("etudiant", "ue", "session")

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code} : {self.moyenne_ue}"


class NoteEC(models.Model):
    resultat_ue = models.ForeignKey(
        ResultatUE, on_delete=models.CASCADE, related_name="notes_ec"
    )
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name="notes")
    valeur = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Note EC"
        verbose_name_plural = "Notes EC"
        unique_together = ("resultat_ue", "ec")

    def __str__(self):
        return f"{self.ec.code} : {self.valeur}"
