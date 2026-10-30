from django.db import models

class SessionResultat(models.Model):
    semestre = models.ForeignKey('filieres.Semestre', on_delete=models.CASCADE)
    specialite = models.ForeignKey('filieres.Specialite', on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=30)

    class Meta:
        db_table = 'session_resultat'

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

class EC(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=200)

    class Meta:
        db_table = 'ec'

class Etudiant(models.Model):
    matricule = models.CharField(max_length=30, unique=True, null=True, blank=True)
    annee_promo = models.CharField(max_length=10, null=True, blank=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)

    class Meta:
        db_table = 'etudiant'

class NoteEC(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    ec = models.ForeignKey(EC, on_delete=models.CASCADE)
    import_fichier = models.ForeignKey('imports.ImportFichier', on_delete=models.SET_NULL, null=True, blank=True, db_column='import_id')
    note = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'note_ec'
        unique_together = ('etudiant', 'ec')

class ResultatUE(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    import_fichier = models.ForeignKey('imports.ImportFichier', on_delete=models.SET_NULL, null=True, blank=True, db_column='import_id')
    moyenne_ue = models.DecimalField(max_digits=4, decimal_places=2)
    statut = models.CharField(max_length=5)

    class Meta:
        db_table = 'resultat_ue'
        unique_together = ('etudiant', 'ue')
