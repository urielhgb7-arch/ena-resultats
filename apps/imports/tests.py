from django.test import TestCase
from .models import MappingTemplate

class ImportsModelsTests(TestCase):
    def test_mapping_template(self):
        mapping = MappingTemplate.objects.create(
            nom="Mapping Default",
            mapping_colonnes={"matricule": "A", "nom": "B", "note": "C"}
        )
        self.assertEqual(str(mapping), "Mapping Default")
        self.assertEqual(mapping.mapping_colonnes["matricule"], "A")
