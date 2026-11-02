from django.test import TestCase
from .models import Etudiant

class ResultatsModelsTests(TestCase):
    def test_etudiant_creation(self):
        etudiant = Etudiant.objects.create(
            matricule="20230001",
            nom="Doe",
            prenom="John"
        )
        self.assertEqual(str(etudiant), "20230001 - Doe John")
