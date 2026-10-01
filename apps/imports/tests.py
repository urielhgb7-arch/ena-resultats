from django.test import TestCase
from apps.imports.models import MappingTemplate, ImportFichier, LigneBrute
from django.contrib.auth import get_user_model

class ImportsModelsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email='admin@example.com',
            nom='Admin',
            role='super_admin',
            password='testpassword'
        )
        self.mapping = MappingTemplate.objects.create(
            nom='Template Standard',
            config_colonnes={"matricule": "A", "nom": "B", "prenom": "C"}
        )

    def test_mapping_template_creation(self):
        self.assertEqual(self.mapping.nom, 'Template Standard')
        self.assertEqual(self.mapping.config_colonnes['matricule'], 'A')

    def test_import_fichier_creation(self):
        import_f = ImportFichier.objects.create(
            nom_fichier='resultats_2025.xlsx',
            utilisateur=self.user,
            mapping=self.mapping
        )
        self.assertEqual(import_f.nom_fichier, 'resultats_2025.xlsx')
        self.assertEqual(import_f.statut, 'en_attente')
        self.assertEqual(import_f.utilisateur, self.user)
        self.assertEqual(import_f.mapping, self.mapping)

    def test_ligne_brute_creation(self):
        import_f = ImportFichier.objects.create(nom_fichier='test.xlsx')
        ligne = LigneBrute.objects.create(
            import_fichier=import_f,
            numero_ligne=2,
            donnees_brutes={"A": "MAT001", "B": "Doe", "C": "John"}
        )
        self.assertEqual(ligne.numero_ligne, 2)
        self.assertEqual(ligne.statut_traitement, 'en_attente')
        self.assertEqual(ligne.donnees_brutes['A'], 'MAT001')
