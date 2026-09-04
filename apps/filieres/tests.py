from django.test import TestCase
from apps.core.models import AnneeAcademique, Niveau, Semestre, SessionResultat
from apps.filieres.models import Filiere, Specialite, UE, EC
from datetime import date

class FilieresModelTests(TestCase):
    def setUp(self):
        self.annee = AnneeAcademique.objects.create(libelle="2025-2026")
        self.niveau = Niveau.objects.create(annee=self.annee, libelle="L1")
        self.filiere = Filiere.objects.create(niveau=self.niveau, nom="Gestion", a_des_specialites=False)
        self.specialite = Specialite.objects.create(filiere=self.filiere, nom="Ressources Humaines")

        self.semestre = Semestre.objects.create(filiere=self.filiere, libelle="S1")
        self.session = SessionResultat.objects.create(semestre=self.semestre, type="normale")

        self.ue = UE.objects.create(
            session=self.session,
            code="MGT101",
            nom="Management de Base",
            credits=3,
            date_publication=date(2025, 1, 15)
        )
        self.ec1 = EC.objects.create(ue=self.ue, code="EC1", nom="Theorie")
        self.ec2 = EC.objects.create(ue=self.ue, code="EC2", nom="Pratique")

    def test_filiere_creation(self):
        self.assertEqual(self.filiere.nom, "Gestion")
        self.assertFalse(self.filiere.a_des_specialites)
        self.assertEqual(str(self.filiere), "Gestion (L1)")

    def test_specialite_creation(self):
        self.assertEqual(self.specialite.nom, "Ressources Humaines")
        self.assertEqual(self.specialite.filiere, self.filiere)
        self.assertEqual(str(self.specialite), "Ressources Humaines - Gestion")

    def test_ue_creation(self):
        self.assertEqual(self.ue.code, "MGT101")
        self.assertEqual(self.ue.credits, 3)
        self.assertEqual(self.ue.statut, "brouillon")
        self.assertEqual(str(self.ue), "MGT101 - Management de Base")

    def test_ec_creation(self):
        self.assertEqual(self.ec1.ue, self.ue)
        self.assertEqual(self.ec1.code, "EC1")
        self.assertEqual(str(self.ec1), "EC1 - Theorie")
