from django.db import models
from apps.filieres.models import UE, EC, AnneeAcademique


class SessionResultat(models.Model):
    nom = models.CharField(max_length=50)  # ex: Normale, Rattrapage
    annee_academique = models.ForeignKey(
        AnneeAcademique, on_delete=models.CASCADE, related_name="sessions"
    )

    def __str__(self):
        return f"{self.nom} - {self.annee_academique}"


class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"


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
        help_text="Moyenne figée lors de l'import. Ne pas recalculer.",
    )
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.etudiant} - {self.ue} : {self.moyenne_ue}"


class NoteEC(models.Model):
    etudiant = models.ForeignKey(
        Etudiant, on_delete=models.CASCADE, related_name="notes_ec"
    )
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name="notes")
    session = models.ForeignKey(
        SessionResultat, on_delete=models.CASCADE, related_name="notes_ec"
    )
    note = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.etudiant} - {self.ec} : {self.note}"
