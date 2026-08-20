from django.db import models
from apps.filieres.models import SessionResultat

class UE(models.Model):
    session = models.ForeignKey(SessionResultat, on_delete=models.CASCADE)
    code = models.CharField(max_length=30)
    nom = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()
    fichier_pdf_archive = models.CharField(max_length=300, null=True, blank=True)
    date_publication = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, default='brouillon')

    class Meta:
        db_table = 'ue'
        indexes = [
            models.Index(fields=['session']),
        ]

    def __str__(self):
        return f"{self.code} - {self.nom}"

class EC(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=200)

    class Meta:
        db_table = 'ec'

    def __str__(self):
        return f"{self.code} - {self.nom}"

class Etudiant(models.Model):
    matricule = models.CharField(max_length=30, unique=True, null=True, blank=True)
    annee_promo = models.CharField(max_length=10, null=True, blank=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)

    class Meta:
        db_table = 'etudiant'
        indexes = [
            models.Index(fields=['matricule']),
            models.Index(fields=['nom', 'prenom']),
        ]

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"

class NoteEC(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    ec = models.ForeignKey(EC, on_delete=models.CASCADE)
    import_fichier = models.ForeignKey('imports.ImportFichier', on_delete=models.SET_NULL, null=True, blank=True, db_column='import_id')
    note = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'note_ec'
        unique_together = ('etudiant', 'ec')
        indexes = [
            models.Index(fields=['etudiant']),
        ]

    def __str__(self):
        return f"{self.etudiant} - {self.ec} : {self.note}"

class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    import_fichier = models.ForeignKey('imports.ImportFichier', on_delete=models.SET_NULL, null=True, blank=True, db_column='import_id')
    moyenne_ue = models.DecimalField(max_digits=4, decimal_places=2)
    statut = models.CharField(max_length=5)

    class Meta:
        db_table = 'resultat_ue'
        unique_together = ('etudiant', 'ue')
        indexes = [
            models.Index(fields=['etudiant']),
        ]

    def __str__(self):
        return f"{self.etudiant} - {self.ue} : {self.moyenne_ue} ({self.statut})"
