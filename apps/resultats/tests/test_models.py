from django.test import TestCase
from apps.resultats.models import SessionResultat, Etudiant, ResultatUE, NoteEC
from apps.filieres.models import AnneeAcademique, Niveau, Semestre, UE, EC
from decimal import Decimal


class ResultatsModelsTest(TestCase):
    def setUp(self):
        self.annee = AnneeAcademique.objects.create(annee="2023-2024")
        self.session = SessionResultat.objects.create(
            nom="Normale", annee_academique=self.annee
        )
        self.etudiant = Etudiant.objects.create(
            matricule="M123", nom="Doe", prenom="John"
        )
        self.niveau = Niveau.objects.create(nom="L1")
        self.semestre = Semestre.objects.create(nom="S1", niveau=self.niveau)
        self.ue = UE.objects.create(
            code="UE1", intitule="Maths", credits=6, semestre=self.semestre
        )
        self.ec = EC.objects.create(code="EC1", intitule="Algèbre", ue=self.ue)

    def test_session_str(self):
        self.assertEqual(str(self.session), "Normale - 2023-2024")

    def test_etudiant_str(self):
        self.assertEqual(str(self.etudiant), "M123 - Doe John")

    def test_resultat_ue_creation(self):
        res = ResultatUE.objects.create(
            etudiant=self.etudiant,
            ue=self.ue,
            session=self.session,
            moyenne_ue=Decimal("15.50"),
            valide=True,
        )
        self.assertEqual(str(res), "M123 - UE1 : 15.50")
        self.assertEqual(res.moyenne_ue, Decimal("15.50"))

    def test_note_ec_creation(self):
        note = NoteEC.objects.create(
            etudiant=self.etudiant,
            ec=self.ec,
            session=self.session,
            note=Decimal("14.00"),
        )
        self.assertEqual(str(note), "M123 - EC1 : 14.00")
        self.assertEqual(note.note, Decimal("14.00"))
