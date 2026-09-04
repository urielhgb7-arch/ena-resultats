from django.test import TestCase
from apps.imports.models import MappingTemplate, ImportFichier, LigneBrute
from django.contrib.auth import get_user_model

class ImportsModelTests(TestCase):
    def setUp(self):
        self.mapping = MappingTemplate.objects.create(
            nom="Template Standard", config_colonnes={"matricule": "A", "note": "B"}
        )
        User = get_user_model()
        self.user = User.objects.create_user(email="admin@test.com", nom="Admin", role="super_admin", password="pass")

        self.import_file = ImportFichier.objects.create(
            nom_fichier="resultats.xlsx", utilisateur=self.user, mapping=self.mapping
        )

        self.ligne = LigneBrute.objects.create(
            import_fichier=self.import_file, numero_ligne=2, donnees_brutes={"A": "123", "B": "15"}
        )

    def test_mapping_template_creation(self):
        self.assertEqual(self.mapping.nom, "Template Standard")
        self.assertEqual(self.mapping.config_colonnes["matricule"], "A")
        self.assertEqual(str(self.mapping), "Template Standard")

    def test_import_fichier_creation(self):
        self.assertEqual(self.import_file.nom_fichier, "resultats.xlsx")
        self.assertEqual(self.import_file.statut, "en_attente")
        self.assertEqual(self.import_file.utilisateur, self.user)
        self.assertIn("resultats.xlsx", str(self.import_file))

    def test_ligne_brute_creation(self):
        self.assertEqual(self.ligne.numero_ligne, 2)
        self.assertEqual(self.ligne.donnees_brutes["A"], "123")
        self.assertEqual(self.ligne.statut_traitement, "en_attente")
        self.assertIn("Ligne 2", str(self.ligne))
