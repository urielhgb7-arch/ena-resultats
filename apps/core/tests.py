from django.test import TestCase
from apps.core.models import AnneeAcademique, Niveau, Semestre, SessionResultat
from apps.filieres.models import Filiere, Specialite

class CoreModelTests(TestCase):
    def setUp(self):
        self.annee = AnneeAcademique.objects.create(libelle="2025-2026", active=True)
        self.niveau = Niveau.objects.create(annee=self.annee, libelle="L1")
        self.filiere = Filiere.objects.create(niveau=self.niveau, nom="Informatique")
        self.specialite = Specialite.objects.create(filiere=self.filiere, nom="Genie Logiciel")
        self.semestre = Semestre.objects.create(filiere=self.filiere, libelle="Semestre 1")
        self.session_resultat = SessionResultat.objects.create(semestre=self.semestre, type="normale")
        self.session_specialite = SessionResultat.objects.create(
            semestre=self.semestre, specialite=self.specialite, type="rattrapage"
        )

    def test_annee_academique_creation(self):
        self.assertEqual(self.annee.libelle, "2025-2026")
        self.assertTrue(self.annee.active)
        self.assertEqual(str(self.annee), "2025-2026")

    def test_niveau_creation(self):
        self.assertEqual(self.niveau.libelle, "L1")
        self.assertEqual(self.niveau.annee, self.annee)
        self.assertEqual(str(self.niveau), "L1 (2025-2026)")

    def test_semestre_creation(self):
        self.assertEqual(self.semestre.libelle, "Semestre 1")
        self.assertEqual(self.semestre.filiere, self.filiere)
        self.assertEqual(self.semestre.type, "normal")
        self.assertEqual(str(self.semestre), "Semestre 1 - Informatique")

    def test_session_resultat_creation(self):
        self.assertEqual(self.session_resultat.semestre, self.semestre)
        self.assertIsNone(self.session_resultat.specialite)
        self.assertEqual(self.session_resultat.type, "normale")
        self.assertEqual(str(self.session_resultat), "Session Normale - Semestre 1")

    def test_session_resultat_with_specialite(self):
        self.assertEqual(self.session_specialite.specialite, self.specialite)
        self.assertEqual(str(self.session_specialite), "Session Rattrapage - Semestre 1 (Genie Logiciel)")
