from django.test import TestCase
from apps.filieres.models import AnneeAcademique, Niveau, Filiere

class FilieresModelsTests(TestCase):
    def test_annee_academique_str(self):
        annee = AnneeAcademique(libelle='2025-2026')
        self.assertEqual(str(annee), '2025-2026')

    def test_filiere_str(self):
        annee = AnneeAcademique.objects.create(libelle='2025-2026')
        niveau = Niveau.objects.create(annee=annee, libelle='L1')
        filiere = Filiere(niveau=niveau, nom='Mathématiques')
        self.assertEqual(str(filiere), 'Mathématiques - L1')
