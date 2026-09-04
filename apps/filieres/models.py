from django.db import models

class Filiere(models.Model):
    niveau = models.ForeignKey('core.Niveau', on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    a_des_specialites = models.BooleanField(default=True)
    specialite_unique_auto = models.BooleanField(default=False)

    class Meta:
        db_table = 'filiere'

    def __str__(self):
        return f"{self.nom} ({self.niveau.libelle})"

class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)

    class Meta:
        db_table = 'specialite'

    def __str__(self):
        return f"{self.nom} - {self.filiere.nom}"

class UE(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]

    session = models.ForeignKey('core.SessionResultat', on_delete=models.CASCADE)
    code = models.CharField(max_length=30)
    nom = models.CharField(max_length=200)
    credits = models.PositiveIntegerField() # Database CHECK (credits > 0) could be added via models.CheckConstraint in Meta
    fichier_pdf_archive = models.FileField(upload_to='archives_pv/', max_length=300, null=True, blank=True)
    date_publication = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')

    class Meta:
        db_table = 'ue'
        constraints = [
            models.CheckConstraint(check=models.Q(credits__gt=0), name='check_credits_positive')
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
