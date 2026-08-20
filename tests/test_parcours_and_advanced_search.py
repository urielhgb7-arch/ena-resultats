from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse

from apps.filieres.models import AnneeAcademique, Niveau, Filiere, Semestre, SessionResultat
from apps.resultats.models import UE, EC, Etudiant, ResultatUE, NoteEC


class ParcoursAndAdvancedSearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Année et Niveaux
        self.annee = AnneeAcademique.objects.create(libelle="2025-2026", active=True)
        self.l1 = Niveau.objects.create(annee=self.annee, libelle="L1")
        self.l2 = Niveau.objects.create(annee=self.annee, libelle="L2")

        # Filière
        self.filiere = Filiere.objects.create(niveau=self.l1, nom="Administration des Finances")
        self.filiere_l2 = Filiere.objects.create(niveau=self.l2, nom="Administration des Finances (L2)")

        # Semestres
        self.s1 = Semestre.objects.create(filiere=self.filiere, libelle="Semestre 1")
        self.s2 = Semestre.objects.create(filiere=self.filiere, libelle="Semestre 2")
        self.s3 = Semestre.objects.create(filiere=self.filiere_l2, libelle="Semestre 3")

        # Sessions
        self.session_s1 = SessionResultat.objects.create(semestre=self.s1, type="normale")
        self.session_s2 = SessionResultat.objects.create(semestre=self.s2, type="normale")
        self.session_s3 = SessionResultat.objects.create(semestre=self.s3, type="normale")

        # UEs
        self.ue_s1 = UE.objects.create(session=self.session_s1, code="UE101", nom="Droit Constitutionnel", credits=4, statut="publie")
        self.ue_s2 = UE.objects.create(session=self.session_s2, code="UE201", nom="Finances Publiques", credits=6, statut="publie")
        self.ue_s3 = UE.objects.create(session=self.session_s3, code="UE301", nom="Fiscalité Appliquée", credits=5, statut="publie")

        # Étudiant avec parcours multi-niveaux (L1 et L2)
        self.etudiant = Etudiant.objects.create(
            matricule="ENA20231000",
            nom="MOUSSAVOU",
            prenom="Alain",
            annee_promo="2023"
        )

        # Résultats
        ResultatUE.objects.create(etudiant=self.etudiant, ue=self.ue_s1, moyenne_ue=Decimal("13.50"), statut="V")
        ResultatUE.objects.create(etudiant=self.etudiant, ue=self.ue_s2, moyenne_ue=Decimal("14.00"), statut="V*")
        ResultatUE.objects.create(etudiant=self.etudiant, ue=self.ue_s3, moyenne_ue=Decimal("9.00"), statut="NV")

    def test_multi_level_consultation_l1_l3(self):
        """Vérifie le regroupement des notes de L1 à L3 et le calcul cumulé des crédits ECTS."""
        url = reverse("resultats:recherche_personnelle")
        response = self.client.get(url, {"q": "MOUSSAVOU", "mode": "nom"})
        self.assertEqual(response.status_code, 200)

        data = response.context["etudiants_data"]
        self.assertEqual(len(data), 1)

        etu_info = data[0]
        self.assertEqual(etu_info["etudiant"], self.etudiant)
        # Total crédits validés (4 + 6 = 10 crédits, la 3ème étant NV)
        self.assertEqual(etu_info["credits_valides"], 10)
        self.assertEqual(etu_info["credits_inscrits"], 15)

        # Vérifie la présence des niveaux L1 et L2 dans l'arbre
        self.assertIn("L1", etu_info["niveaux_tree"])
        self.assertIn("L2", etu_info["niveaux_tree"])

    def test_recherche_avancee_page(self):
        url = reverse("resultats:recherche_avancee")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recherche Directe")
        self.assertContains(response, "2025-2026")

    def test_ajax_cascade_endpoints(self):
        # 1. AJAX Niveaux
        res_niv = self.client.get(reverse("filieres:ajax_niveaux"), {"annee_id": self.annee.id})
        self.assertEqual(res_niv.status_code, 200)
        self.assertContains(res_niv, "L1")
        self.assertContains(res_niv, "L2")

        # 2. AJAX Filières
        res_fil = self.client.get(reverse("filieres:ajax_filieres"), {"niveau_id": self.l1.id})
        self.assertEqual(res_fil.status_code, 200)
        self.assertContains(res_fil, "Administration des Finances")

        # 3. AJAX Semestres
        res_sem = self.client.get(reverse("filieres:ajax_semestres"), {"filiere_id": self.filiere.id})
        self.assertEqual(res_sem.status_code, 200)
        self.assertContains(res_sem, "Semestre 1")
        self.assertContains(res_sem, "Semestre 2")

    def test_recherche_avancee_redirection(self):
        url = reverse("resultats:recherche_avancee")
        response = self.client.get(url, {
            "annee_id": self.annee.id,
            "niveau_id": self.l1.id,
            "filiere_id": self.filiere.id,
            "semestre_id": self.s1.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("filieres:sessions", args=[self.s1.id]))
