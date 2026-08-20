from django.test import TestCase
from apps.filieres.models import AnneeAcademique, Niveau, Filiere, Semestre, SessionResultat
from apps.resultats.models import UE, Etudiant

class ResultatsModelsTests(TestCase):
    def setUp(self):
        annee = AnneeAcademique.objects.create(libelle='2025-2026')
        niveau = Niveau.objects.create(annee=annee, libelle='L1')
        filiere = Filiere.objects.create(niveau=niveau, nom='Informatique')
        semestre = Semestre.objects.create(filiere=filiere, libelle='Semestre 1')
        self.session = SessionResultat.objects.create(semestre=semestre, type='normale')

    def test_ue_str(self):
        ue = UE(session=self.session, code='INF101', nom='Introduction à la programmation', credits=6)
        self.assertEqual(str(ue), 'INF101 - Introduction à la programmation')

    def test_etudiant_str(self):
        etudiant = Etudiant(matricule='250001', nom='Dupont', prenom='Jean')
        self.assertEqual(str(etudiant), 'Dupont Jean (250001)')
