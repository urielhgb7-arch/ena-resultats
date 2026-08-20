from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse

from apps.filieres.models import AnneeAcademique, Niveau, Filiere, Semestre, SessionResultat
from apps.resultats.models import UE, EC, Etudiant, ResultatUE, NoteEC


class ResultsAndSearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Configuration académique
        self.annee = AnneeAcademique.objects.create(libelle="2025-2026", active=True)
        self.niveau = Niveau.objects.create(annee=self.annee, libelle="L1")
        self.filiere = Filiere.objects.create(niveau=self.niveau, nom="Administration Générale")
        self.semestre = Semestre.objects.create(filiere=self.filiere, libelle="Semestre 1")
        self.session = SessionResultat.objects.create(semestre=self.semestre, type="normale")

        self.ue = UE.objects.create(
            session=self.session,
            code="DRT1101",
            nom="Droit Administratif",
            credits=4,
            statut="publie"
        )
        self.ue_brouillon = UE.objects.create(
            session=self.session,
            code="MTH1102",
            nom="Statistiques Descriptives",
            credits=3,
            statut="brouillon"
        )

        self.ec1 = EC.objects.create(ue=self.ue, code="EC1", nom="Droit Constitutionnel")
        self.ec2 = EC.objects.create(ue=self.ue, code="EC2", nom="Organisation Administrative")

        # Étudiants
        self.etu1 = Etudiant.objects.create(
            matricule="ENA2025001",
            nom="ADANHO",
            prenom="Céline",
            annee_promo="2025"
        )
        self.etu2 = Etudiant.objects.create(
            matricule="ENA2025002",
            nom="ZOSSOU",
            prenom="Boris",
            annee_promo="2025"
        )

        # Résultats et notes
        ResultatUE.objects.create(
            etudiant=self.etu1,
            ue=self.ue,
            moyenne_ue=Decimal("15.50"),
            statut="V"
        )
        NoteEC.objects.create(etudiant=self.etu1, ec=self.ec1, note=Decimal("16.00"))
        NoteEC.objects.create(etudiant=self.etu1, ec=self.ec2, note=Decimal("15.00"))

        ResultatUE.objects.create(
            etudiant=self.etu2,
            ue=self.ue,
            moyenne_ue=Decimal("8.50"),
            statut="NV"
        )
        NoteEC.objects.create(etudiant=self.etu2, ec=self.ec1, note=Decimal("8.00"))
        NoteEC.objects.create(etudiant=self.etu2, ec=self.ec2, note=Decimal("9.00"))

    def test_ue_detail_public_view_and_stats(self):
        url = reverse("resultats:ue_detail", args=[self.ue.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Droit Administratif")
        self.assertContains(response, "ADANHO")
        self.assertContains(response, "ZOSSOU")
        self.assertContains(response, "15,50")
        self.assertContains(response, "8,50")
        
        # Vérification des stats
        self.assertEqual(response.context["total_etudiants"], 2)
        self.assertEqual(response.context["valides_count"], 1)
        self.assertEqual(response.context["taux_reussite"], 50.0)

    def test_ue_brouillon_is_not_accessible(self):
        url = reverse("resultats:ue_detail", args=[self.ue_brouillon.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_ue_local_search_filter(self):
        url = reverse("resultats:ue_classement", args=[self.ue.id])
        response = self.client.get(url, {"q": "ADANHO"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ADANHO")
        self.assertNotContains(response, "ZOSSOU")

    def test_ue_sorting_order(self):
        # Tri par mérite (note max en premier)
        url = reverse("resultats:ue_classement", args=[self.ue.id])
        response = self.client.get(url, {"tri": "moyenne_desc"})
        self.assertEqual(response.status_code, 200)
        resultats = response.context["resultats"]
        self.assertEqual(resultats[0].etudiant, self.etu1)
        self.assertEqual(resultats[1].etudiant, self.etu2)

    def test_ue_htmx_partial_response(self):
        url = reverse("resultats:ue_classement", args=[self.ue.id])
        response = self.client.get(url, {"q": "Céline"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resultats/partials/ue_table_rows.html")
        self.assertContains(response, "ADANHO")

    def test_personal_search_by_matricule(self):
        url = reverse("resultats:recherche_personnelle")
        response = self.client.get(url, {"q": "ENA2025001", "mode": "matricule"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ADANHO Céline")
        self.assertContains(response, "Crédits ECTS validés")
        self.assertContains(response, "15,50")
        self.assertNotContains(response, "ZOSSOU Boris")

    def test_personal_search_by_name(self):
        url = reverse("resultats:recherche_personnelle")
        response = self.client.get(url, {"q": "Zossou", "mode": "nom"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ZOSSOU Boris")
        self.assertNotContains(response, "ADANHO Céline")

    def test_personal_search_htmx_partial_response(self):
        url = reverse("resultats:recherche_personnelle")
        response = self.client.get(url, {"q": "ADANHO"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resultats/partials/recherche_results.html")
