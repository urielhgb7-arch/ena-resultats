from django.test import TestCase
from .models import AnneeAcademique, Niveau, Filiere

class FiliereModelsTests(TestCase):
    def test_annee_academique(self):
        annee = AnneeAcademique.objects.create(
            annee="2023-2024",
            en_cours=True,
            date_debut="2023-09-01",
            date_fin="2024-07-31"
        )
        self.assertEqual(str(annee), "2023-2024")

    def test_niveau_filiere(self):
        niveau = Niveau.objects.create(code="L1", nom="Licence 1")
        filiere = Filiere.objects.create(code="INF", nom="Informatique")
        self.assertEqual(str(niveau), "L1")
        self.assertEqual(str(filiere), "Informatique")
