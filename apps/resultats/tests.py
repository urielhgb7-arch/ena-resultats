from django.test import TestCase
from .models import SessionResultat, UE, EC, Etudiant, NoteEC, ResultatUE
from apps.filieres.models import AnneeAcademique, Niveau, Filiere, Semestre
from decimal import Decimal

class ResultatsModelsTests(TestCase):
    def setUp(self):
        self.annee = AnneeAcademique.objects.create(libelle="2023-2024")
        self.filiere = Filiere.objects.create(nom="Informatique", code="INFO")
        self.niveau = Niveau.objects.create(libelle="L1", ordre=1)
        self.semestre = Semestre.objects.create(numero=1, niveau=self.niveau)
        self.session = SessionResultat.objects.create(
            annee_academique=self.annee,
            semestre=self.semestre,
            filiere=self.filiere,
            type_session=SessionResultat.TypeSession.NORMALE,
        )
        self.etudiant = Etudiant.objects.create(matricule="12345", nom="Doe", prenom="John")
        self.ue = UE.objects.create(code="UE1", intitule="Mathématiques", credits=6, session=self.session)

    def test_resultat_ue_moyenne_figee(self):
        # ResultatUE.moyenne_ue should be a fixed field, set explicitly and not dynamically calculated.
        resultat = ResultatUE.objects.create(etudiant=self.etudiant, ue=self.ue, moyenne_ue=Decimal('15.50'))
        self.assertEqual(resultat.moyenne_ue, Decimal('15.50'))

    def test_ec_creation_and_notes(self):
        ec = EC.objects.create(code="EC1.1", intitule="Algèbre", ue=self.ue)
        note = NoteEC.objects.create(etudiant=self.etudiant, ec=ec, valeur=Decimal('16.00'))
        self.assertEqual(note.valeur, Decimal('16.00'))
        self.assertEqual(note.ec.ue, self.ue)
