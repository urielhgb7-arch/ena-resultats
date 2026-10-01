from django.test import TestCase
from django.db import IntegrityError
from apps.resultats.models import Etudiant, ResultatUE, NoteEC
from apps.core.models import AnneeAcademique, Niveau, Semestre, SessionResultat
from apps.filieres.models import Filiere, UE, EC

class ResultatsModelsTests(TestCase):
    def setUp(self):
        self.etudiant = Etudiant.objects.create(
            matricule='MAT001',
            nom='Doe',
            prenom='John'
        )
        self.annee = AnneeAcademique.objects.create(libelle='2025-2026')
        self.niveau = Niveau.objects.create(annee=self.annee, libelle='L1')
        self.filiere = Filiere.objects.create(niveau=self.niveau, nom='Info')
        self.semestre = Semestre.objects.create(filiere=self.filiere, libelle='S1')
        self.session = SessionResultat.objects.create(semestre=self.semestre, type='normale')

        self.ue = UE.objects.create(session=self.session, code='UE1', nom='UE1', credits=6)
        self.ec = EC.objects.create(ue=self.ue, code='EC1', nom='EC1')

    def test_etudiant_creation(self):
        self.assertEqual(self.etudiant.matricule, 'MAT001')
        self.assertEqual(self.etudiant.nom, 'Doe')

    def test_etudiant_unique_matricule(self):
        with self.assertRaises(IntegrityError):
            Etudiant.objects.create(matricule='MAT001', nom='Smith', prenom='Jane')

    def test_note_ec_creation(self):
        note = NoteEC.objects.create(
            etudiant=self.etudiant,
            ec=self.ec,
            note=15.5
        )
        self.assertEqual(note.note, 15.5)
        self.assertEqual(note.etudiant, self.etudiant)

    def test_note_ec_unique_together(self):
        NoteEC.objects.create(etudiant=self.etudiant, ec=self.ec, note=15.5)
        with self.assertRaises(IntegrityError):
            NoteEC.objects.create(etudiant=self.etudiant, ec=self.ec, note=12.0)

    def test_resultat_ue_creation(self):
        resultat = ResultatUE.objects.create(
            etudiant=self.etudiant,
            ue=self.ue,
            moyenne_ue=14.0,
            statut='V'
        )
        self.assertEqual(resultat.moyenne_ue, 14.0)
        self.assertEqual(resultat.statut, 'V')

    def test_resultat_ue_unique_together(self):
        ResultatUE.objects.create(etudiant=self.etudiant, ue=self.ue, moyenne_ue=14.0, statut='V')
        with self.assertRaises(IntegrityError):
            ResultatUE.objects.create(etudiant=self.etudiant, ue=self.ue, moyenne_ue=10.0, statut='NV')
