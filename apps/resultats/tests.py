from django.test import TestCase
from apps.resultats.models import Etudiant, NoteEC, ResultatUE
from apps.core.models import AnneeAcademique, Niveau, Semestre, SessionResultat
from apps.filieres.models import Filiere, UE, EC

class ResultatsModelTests(TestCase):
    def setUp(self):
        self.etudiant = Etudiant.objects.create(
            matricule="26M123", nom="Doe", prenom="John", annee_promo="26"
        )

        # Setup required related objects
        annee = AnneeAcademique.objects.create(libelle="2025-2026")
        niveau = Niveau.objects.create(annee=annee, libelle="L1")
        filiere = Filiere.objects.create(niveau=niveau, nom="Info")
        semestre = Semestre.objects.create(filiere=filiere, libelle="S1")
        session = SessionResultat.objects.create(semestre=semestre, type="normale")
        self.ue = UE.objects.create(session=session, code="UE1", nom="Maths", credits=4)
        self.ec = EC.objects.create(ue=self.ue, code="EC1", nom="Algebre")

        self.note = NoteEC.objects.create(
            etudiant=self.etudiant, ec=self.ec, note=15.5
        )

        self.resultat = ResultatUE.objects.create(
            etudiant=self.etudiant, ue=self.ue, moyenne_ue=14.0, statut="V"
        )

    def test_etudiant_creation(self):
        self.assertEqual(self.etudiant.nom, "Doe")
        self.assertEqual(self.etudiant.matricule, "26M123")
        self.assertEqual(str(self.etudiant), "Doe John (26M123)")

    def test_note_ec_creation(self):
        self.assertEqual(self.note.note, 15.5)
        self.assertEqual(self.note.etudiant, self.etudiant)
        self.assertEqual(self.note.ec, self.ec)

    def test_resultat_ue_creation(self):
        self.assertEqual(self.resultat.moyenne_ue, 14.0)
        self.assertEqual(self.resultat.statut, "V")
        self.assertEqual(self.resultat.etudiant, self.etudiant)
        self.assertEqual(self.resultat.ue, self.ue)
