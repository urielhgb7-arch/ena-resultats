from django.db import models
from apps.filieres.models import AnneeAcademique, Semestre, Etudiant, UE, EC


class SessionResultat(models.Model):
    annee_academique = models.ForeignKey(
        AnneeAcademique, on_delete=models.CASCADE, related_name="sessions"
    )
    semestre = models.ForeignKey(
        Semestre, on_delete=models.CASCADE, related_name="sessions"
    )
    date_publication = models.DateTimeField(null=True, blank=True)
    est_publie = models.BooleanField(default=False)

    class Meta:
        unique_together = ("annee_academique", "semestre")

    def __str__(self):
        return f"{self.semestre.nom} - {self.annee_academique.annee}"


class ResultatUE(models.Model):
    session = models.ForeignKey(
        SessionResultat, on_delete=models.CASCADE, related_name="resultats_ue"
    )
    etudiant = models.ForeignKey(
        Etudiant, on_delete=models.CASCADE, related_name="resultats_ue"
    )
    ue = models.ForeignKey(
        UE, on_delete=models.CASCADE, related_name="resultats_etudiants"
    )
    moyenne_ue = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Figée à l'import, jamais recalculée"
    )

    class Meta:
        unique_together = ("session", "etudiant", "ue")

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code} : {self.moyenne_ue}"


class NoteEC(models.Model):
    resultat_ue = models.ForeignKey(
        ResultatUE, on_delete=models.CASCADE, related_name="notes_ec"
    )
    ec = models.ForeignKey(EC, on_delete=models.CASCADE, related_name="notes")
    note = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("resultat_ue", "ec")

    def __str__(self):
        return f"{self.resultat_ue.etudiant.matricule} - {self.ec.code} : {self.note}"
