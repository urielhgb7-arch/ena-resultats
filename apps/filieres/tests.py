from django.test import TestCase
from apps.core.models import AnneeAcademique, Niveau, Semestre, SessionResultat
from apps.filieres.models import Filiere, Specialite, UE, EC

class FilieresModelsTests(TestCase):
    def setUp(self):
        self.annee = AnneeAcademique.objects.create(libelle='2025-2026')
        self.niveau = Niveau.objects.create(annee=self.annee, libelle='L1')
        self.filiere = Filiere.objects.create(niveau=self.niveau, nom='Informatique', a_des_specialites=True)
        self.semestre = Semestre.objects.create(filiere=self.filiere, libelle='Semestre 1')
        self.session = SessionResultat.objects.create(semestre=self.semestre, type='normale')

    def test_filiere_creation(self):
        self.assertEqual(self.filiere.nom, 'Informatique')
        self.assertTrue(self.filiere.a_des_specialites)

    def test_specialite_creation(self):
        specialite = Specialite.objects.create(filiere=self.filiere, nom='Genie Logiciel')
        self.assertEqual(specialite.nom, 'Genie Logiciel')
        self.assertEqual(specialite.filiere, self.filiere)

    def test_ue_creation(self):
        ue = UE.objects.create(
            session=self.session,
            code='INF101',
            nom='Algorithmique',
            credits=6
        )
        self.assertEqual(ue.code, 'INF101')
        self.assertEqual(ue.credits, 6)

    def test_ec_creation(self):
        ue = UE.objects.create(session=self.session, code='INF101', nom='Algorithmique', credits=6)
        ec = EC.objects.create(ue=ue, code='EC1', nom='Introduction')
        self.assertEqual(ec.code, 'EC1')
        self.assertEqual(ec.ue, ue)
