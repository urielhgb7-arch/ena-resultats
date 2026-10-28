from django.test import TestCase
from .models import ImportFichier, LigneBrute, MappingTemplate
from apps.resultats.models import SessionResultat
from apps.filieres.models import AnneeAcademique, Niveau, Semestre, Filiere

class ImportsModelsTests(TestCase):
    def setUp(self):
        annee = AnneeAcademique.objects.create(libelle="2023-2024")
        niveau = Niveau.objects.create(libelle="L1", ordre=1)
        semestre = Semestre.objects.create(numero=1, niveau=niveau)
        filiere = Filiere.objects.create(nom="Informatique", code="INFO")
        self.session = SessionResultat.objects.create(
            annee_academique=annee,
            semestre=semestre,
            filiere=filiere
        )

    def test_import_fichier_creation(self):
        import_obj = ImportFichier.objects.create(session=self.session, statut=ImportFichier.Statut.EN_ATTENTE)
        self.assertEqual(import_obj.statut, ImportFichier.Statut.EN_ATTENTE)

    def test_ligne_brute_creation(self):
        import_obj = ImportFichier.objects.create(session=self.session)
        ligne = LigneBrute.objects.create(
            import_fichier=import_obj,
            numero_ligne=1,
            donnees={"Matricule": "123", "Note": "15"}
        )
        self.assertEqual(ligne.numero_ligne, 1)
        self.assertEqual(ligne.donnees["Matricule"], "123")

    def test_mapping_template(self):
        template = MappingTemplate.objects.create(
            nom="Template Standard",
            mapping={"matricule": "A", "nom": "B", "note": "C"}
        )
        self.assertEqual(template.mapping["matricule"], "A")
