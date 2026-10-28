from django.test import TestCase
from .models import AnneeAcademique, Niveau, Filiere, Specialite, Semestre

class FiliereModelsTests(TestCase):
    def test_annee_academique_creation(self):
        annee = AnneeAcademique.objects.create(libelle="2023-2024", en_cours=True)
        self.assertEqual(annee.libelle, "2023-2024")
        self.assertTrue(annee.en_cours)

    def test_niveau_creation(self):
        niveau = Niveau.objects.create(libelle="L1", ordre=1)
        self.assertEqual(niveau.libelle, "L1")

    def test_filiere_specialite_relation(self):
        filiere = Filiere.objects.create(nom="Informatique", code="INFO", a_des_specialites=True)
        specialite = Specialite.objects.create(filiere=filiere, nom="Génie Logiciel", code="GL")
        self.assertEqual(filiere.specialites.count(), 1)
        self.assertEqual(specialite.filiere, filiere)

    def test_semestre_niveau_relation(self):
        niveau = Niveau.objects.create(libelle="L1", ordre=1)
        semestre = Semestre.objects.create(numero=1, niveau=niveau)
        self.assertEqual(semestre.niveau, niveau)
