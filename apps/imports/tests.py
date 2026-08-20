from django.test import TestCase
from apps.imports.models import MappingTemplate

class ImportsModelsTests(TestCase):
    def test_mapping_template_str(self):
        mapping = MappingTemplate(nom='Template Standard', config_colonnes={})
        self.assertEqual(str(mapping), 'Template Standard')
