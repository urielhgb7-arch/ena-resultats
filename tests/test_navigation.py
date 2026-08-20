from django.test import TestCase, Client
from django.urls import reverse

from apps.filieres.models import AnneeAcademique, Niveau, Filiere, Specialite, Semestre, SessionResultat
from apps.resultats.models import UE, EC


class NavigationTreeTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # 1. Années
        self.annee_active = AnneeAcademique.objects.create(libelle="2025-2026", active=True)
        self.annee_archive = AnneeAcademique.objects.create(libelle="2024-2025", active=False)

        # 2. Niveaux
        self.l1 = Niveau.objects.create(annee=self.annee_active, libelle="L1")
        self.l2 = Niveau.objects.create(annee=self.annee_active, libelle="L2")

        # 3. Filières et cas d'exceptions métier
        # Cas 1 : Filière standard avec plusieurs spécialités
        self.filiere_standard = Filiere.objects.create(
            niveau=self.l1,
            nom="Administration Générale et Territoriale",
            a_des_specialites=True,
            specialite_unique_auto=False
        )
        self.spec1 = Specialite.objects.create(filiere=self.filiere_standard, nom="Diplomatie")
        self.spec2 = Specialite.objects.create(filiere=self.filiere_standard, nom="Administration Centrale")

        # Cas 2 : Filière sans spécialité (Secrétariat de Gestion)
        self.filiere_sans_spec = Filiere.objects.create(
            niveau=self.l1,
            nom="Secrétariat de Gestion",
            a_des_specialites=False,
            specialite_unique_auto=False
        )

        # Cas 3 : Filière avec spécialité unique automatique (STID)
        self.filiere_stid = Filiere.objects.create(
            niveau=self.l1,
            nom="Statistique et Informatique Décisionnelle",
            a_des_specialites=True,
            specialite_unique_auto=True
        )
        self.spec_stid = Specialite.objects.create(filiere=self.filiere_stid, nom="Statistique Décisionnelle")

        # 4. Semestres et Sessions
        self.semestre_s1 = Semestre.objects.create(filiere=self.filiere_standard, libelle="Semestre 1")
        self.semestre_sans_spec = Semestre.objects.create(filiere=self.filiere_sans_spec, libelle="Semestre 1")
        self.semestre_stid = Semestre.objects.create(filiere=self.filiere_stid, libelle="Semestre 1")

        self.session_normale = SessionResultat.objects.create(
            semestre=self.semestre_s1,
            specialite=self.spec1,
            type="normale"
        )

        # 5. UEs (Publiée vs Brouillon)
        self.ue_publiee = UE.objects.create(
            session=self.session_normale,
            code="DRT1101",
            nom="Droit Administratif",
            credits=4,
            statut="publie"
        )
        self.ue_brouillon = UE.objects.create(
            session=self.session_normale,
            code="MTH1102",
            nom="Comptabilité Publique (En cours)",
            credits=3,
            statut="brouillon"
        )

    def test_accueil_view(self):
        url = reverse("filieres:accueil")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2025-2026")
        self.assertContains(response, "2024-2025")
        self.assertContains(response, "L1")

    def test_liste_niveaux(self):
        url = reverse("filieres:niveaux", args=[self.annee_active.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "L1")
        self.assertContains(response, "L2")

    def test_liste_filieres(self):
        url = reverse("filieres:filieres", args=[self.l1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Administration Générale et Territoriale")
        self.assertContains(response, "Secrétariat de Gestion")
        self.assertContains(response, "Statistique et Informatique Décisionnelle")

    def test_specialites_filiere_standard(self):
        url = reverse("filieres:specialites", args=[self.filiere_standard.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Diplomatie")
        self.assertContains(response, "Administration Centrale")

    def test_exception_filiere_sans_specialite_redirects_to_semestres(self):
        """Secrétariat de Gestion n'a pas de spécialités -> saut direct aux semestres."""
        url = reverse("filieres:specialites", args=[self.filiere_sans_spec.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        expected_url = reverse("filieres:semestres", kwargs={"filiere_id": self.filiere_sans_spec.id})
        self.assertRedirects(response, expected_url)

    def test_exception_filiere_specialite_unique_auto_redirects(self):
        """STID a une spécialité unique auto -> saut direct aux semestres avec spécialité pré-sélectionnée."""
        url = reverse("filieres:specialites", args=[self.filiere_stid.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        expected_url = reverse(
            "filieres:semestres_avec_specialite",
            kwargs={"filiere_id": self.filiere_stid.id, "specialite_id": self.spec_stid.id}
        )
        self.assertRedirects(response, expected_url)

    def test_liste_semestres_and_sessions(self):
        # Semestres
        url_sem = reverse("filieres:semestres", args=[self.filiere_standard.id])
        res_sem = self.client.get(url_sem)
        self.assertEqual(res_sem.status_code, 200)
        self.assertContains(res_sem, "Semestre 1")

        # Sessions
        url_sess = reverse("filieres:sessions", args=[self.semestre_s1.id])
        res_sess = self.client.get(url_sess)
        self.assertEqual(res_sess.status_code, 200)
        self.assertContains(res_sess, "Session normale")

    def test_liste_ue_filters_out_drafts(self):
        """Seules les UE publiées doivent être affichées au public."""
        url = reverse("filieres:ue_liste", args=[self.session_normale.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DRT1101")
        self.assertContains(response, "Droit Administratif")
        self.assertNotContains(response, "MTH1102")
        self.assertNotContains(response, "Comptabilité Publique (En cours)")
