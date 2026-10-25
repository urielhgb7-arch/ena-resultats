from django.db import models
from apps.filieres.models import UE, EC


class SessionResultat(models.Model):
    nom = models.CharField(max_length=100)  # ex: "Normale", "Rattrapage"


class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)


class NoteEC(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    ec = models.ForeignKey(EC, on_delete=models.CASCADE)
    valeur = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE)
    moyenne_ue = models.DecimalField(max_digits=5, decimal_places=2)  # Fixed rule!
