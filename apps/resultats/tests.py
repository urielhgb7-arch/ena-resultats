from django.test import TestCase
from apps.filieres.models import AnneeAcademique, Niveau, Semestre, Filiere
from apps.resultats.models import SessionResultat, UE, Etudiant, ResultatUE

class ResultatUETest(TestCase):
    def setUp(self):
        self.annee = AnneeAcademique.objects.create(annee="2023-2024", active=True)
        self.niveau = Niveau.objects.create(nom="L1", ordre=1)
        self.semestre = Semestre.objects.create(nom="S1", niveau=self.niveau)
        self.filiere = Filiere.objects.create(nom="Informatique", code="INFO")

        self.session = SessionResultat.objects.create(
            annee_academique=self.annee,
            semestre=self.semestre,
            type_session='normale'
        )
        self.ue = UE.objects.create(nom="Algorithmique", code="ALG1", credits=5, semestre=self.semestre)
        self.etudiant = Etudiant.objects.create(
            matricule="12345",
            nom="Doe",
            prenom="John",
            filiere=self.filiere
        )

    def test_moyenne_ue_is_saved_and_not_recalculated(self):
        # We explicitly set `moyenne_ue` when creating ResultatUE
        resultat = ResultatUE.objects.create(
            etudiant=self.etudiant,
            ue=self.ue,
            session=self.session,
            moyenne_ue=14.5,
            valide=True
        )

        # Ensure the `moyenne_ue` value is retained exactly as we passed it
        resultat.refresh_from_db()
        self.assertEqual(resultat.moyenne_ue, 14.5)

        # Test updating it, ensuring it acts as a normal field and doesn't fall back to NoteEC calculation
        resultat.moyenne_ue = 16.0
        resultat.save()

        resultat.refresh_from_db()
        self.assertEqual(resultat.moyenne_ue, 16.0)
