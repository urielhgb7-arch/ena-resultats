from django.db import models
from apps.filieres.models import AnneeAcademique, Semestre, Filiere, Specialite
from django.core.validators import MinValueValidator, MaxValueValidator


class SessionResultat(models.Model):
    TYPE_SESSION = (
        ("NORMALE", "Normale"),
        ("RATTRAPAGE", "Rattrapage"),
    )
    type = models.CharField(max_length=20, choices=TYPE_SESSION, default="NORMALE")
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_type_display()} - {self.semestre} - {self.annee_academique}"


class UE(models.Model):
    code = models.CharField(max_length=20)
    intitule = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    specialite = models.ForeignKey(
        Specialite, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.code} - {self.intitule}"


class EC(models.Model):
    code = models.CharField(max_length=20)
    intitule = models.CharField(max_length=200)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name="ecs")
    coefficient = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.code} - {self.intitule}"


class Etudiant(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"


class ResultatUE(models.Model):
    etudiant = models.ForeignKey(
        Etudiant, on_delete=models.CASCADE, related_name="resultats_ue"
    )
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE)
    # Règle non négociable: moyenne_ue est figée et non recalculée dynamiquement
    moyenne_ue = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.etudiant.matricule} - {self.ue.code}: {self.moyenne_ue}"

    class Meta:
        unique_together = ("etudiant", "ue", "session")


class NoteEC(models.Model):
    resultat_ue = models.ForeignKey(
        ResultatUE, on_delete=models.CASCADE, related_name="notes_ec"
    )
    ec = models.ForeignKey(EC, on_delete=models.CASCADE)
    valeur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )

    def __str__(self):
        return f"{self.resultat_ue.etudiant.matricule} - {self.ec.code}: {self.valeur}"

    class Meta:
        unique_together = ("resultat_ue", "ec")
