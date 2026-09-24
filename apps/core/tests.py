from django.test import TestCase
from .models import AnneeAcademique, Niveau

class CoreModelsTest(TestCase):
    def test_annee_academique_creation(self):
        annee = AnneeAcademique.objects.create(libelle='2025-2026', active=True)
        self.assertEqual(annee.libelle, '2025-2026')
        self.assertTrue(annee.active)
        self.assertEqual(str(annee), '2025-2026')

    def test_niveau_creation(self):
        annee = AnneeAcademique.objects.create(libelle='2025-2026')
        niveau = Niveau.objects.create(annee=annee, libelle='L1')
        self.assertEqual(niveau.libelle, 'L1')
        self.assertEqual(niveau.annee, annee)
        self.assertEqual(str(niveau), 'L1 (2025-2026)')
