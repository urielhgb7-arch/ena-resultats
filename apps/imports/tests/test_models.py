from django.test import TestCase
from apps.imports.models import ImportFichier, MappingTemplate, LigneBrute
from apps.resultats.models import SessionResultat
from apps.filieres.models import AnneeAcademique
from django.core.files.uploadedfile import SimpleUploadedFile


class ImportsModelsTest(TestCase):
    def setUp(self):
        self.annee = AnneeAcademique.objects.create(annee="2023-2024")
        self.session = SessionResultat.objects.create(
            nom="Normale", annee_academique=self.annee
        )
        self.file = SimpleUploadedFile(
            "file.xlsx",
            b"file_content",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def test_import_fichier_str(self):
        imp = ImportFichier.objects.create(
            fichier=self.file, session=self.session, statut="EN_ATTENTE"
        )
        self.assertEqual(str(imp), f"Import {imp.id} - En attente")

    def test_mapping_template_str(self):
        mapping = MappingTemplate.objects.create(
            nom="Template 1", mapping_json={"col": "val"}
        )
        self.assertEqual(str(mapping), "Template 1")

    def test_ligne_brute_str(self):
        imp = ImportFichier.objects.create(
            fichier=self.file, session=self.session, statut="EN_ATTENTE"
        )
        ligne = LigneBrute.objects.create(
            import_fichier=imp, donnees_json={"data": "val"}
        )
        self.assertEqual(str(ligne), f"Ligne de l'import {imp.id}")
