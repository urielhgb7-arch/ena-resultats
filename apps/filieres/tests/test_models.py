from django.test import TestCase
from apps.filieres.models import (
    AnneeAcademique,
    Niveau,
    Filiere,
    Specialite,
    Semestre,
    UE,
    EC,
)


class FiliereModelsTest(TestCase):
    def test_annee_academique_str(self):
        annee = AnneeAcademique.objects.create(annee="2023-2024")
        self.assertEqual(str(annee), "2023-2024")

    def test_niveau_str(self):
        niveau = Niveau.objects.create(nom="L1")
        self.assertEqual(str(niveau), "L1")

    def test_filiere_str(self):
        filiere = Filiere.objects.create(nom="Informatique", a_des_specialites=True)
        self.assertEqual(str(filiere), "Informatique")

    def test_specialite_str(self):
        filiere = Filiere.objects.create(nom="Informatique")
        spec = Specialite.objects.create(nom="Dev Web", filiere=filiere)
        self.assertEqual(str(spec), "Informatique - Dev Web")

    def test_semestre_str(self):
        niveau = Niveau.objects.create(nom="L1")
        sem = Semestre.objects.create(nom="S1", niveau=niveau)
        self.assertEqual(str(sem), "S1 (L1)")

    def test_ue_str(self):
        niveau = Niveau.objects.create(nom="L1")
        sem = Semestre.objects.create(nom="S1", niveau=niveau)
        ue = UE.objects.create(code="UE1", intitule="Maths", credits=6, semestre=sem)
        self.assertEqual(str(ue), "UE1 - Maths")

    def test_ec_str(self):
        niveau = Niveau.objects.create(nom="L1")
        sem = Semestre.objects.create(nom="S1", niveau=niveau)
        ue = UE.objects.create(code="UE1", intitule="Maths", credits=6, semestre=sem)
        ec = EC.objects.create(code="EC1", intitule="Algèbre", ue=ue)
        self.assertEqual(str(ec), "EC1 - Algèbre")
