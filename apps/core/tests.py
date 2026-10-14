from django.test import TestCase
from apps.core.models import AnneeAcademique

class CoreModelsTest(TestCase):
    def test_annee_academique_creation(self):
        annee = AnneeAcademique.objects.create(libelle="2025-2026", active=True)
        self.assertEqual(annee.libelle, "2025-2026")
        self.assertTrue(annee.active)
