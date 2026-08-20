import tempfile
from decimal import Decimal
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import openpyxl

from apps.accounts.models import UtilisateurAdmin
from apps.filieres.models import AnneeAcademique, Niveau, Filiere, Semestre, SessionResultat
from apps.imports.models import ImportFichier, LigneBrute, MappingTemplate
from apps.imports.tasks import clean_decimal, process_import_staging_task, process_import_validation_task
from apps.resultats.models import Etudiant, UE, EC, ResultatUE, NoteEC


class ImportPipelineTestCase(TestCase):
    def setUp(self):
        # 1. Données référentielles
        self.user = UtilisateurAdmin.objects.create_user(
            email="admin.import@ena.bj",
            nom="Admin Import",
            role="super_admin",
            password="securePassword123!"
        )
        self.annee = AnneeAcademique.objects.create(libelle="2025-2026", active=True)
        self.niveau = Niveau.objects.create(annee=self.annee, libelle="L1")
        self.filiere = Filiere.objects.create(niveau=self.niveau, nom="Administration Générale")
        self.semestre = Semestre.objects.create(filiere=self.filiere, libelle="Semestre 1")
        self.session = SessionResultat.objects.create(semestre=self.semestre, type="normale")

        self.ue = UE.objects.create(
            session=self.session,
            code="MTH1101",
            nom="Mathématiques et Statistiques",
            credits=4,
            statut="publie"
        )
        self.ec1 = EC.objects.create(ue=self.ue, code="EC1", nom="Mathématiques Générales")
        self.ec2 = EC.objects.create(ue=self.ue, code="EC2", nom="Statistiques")

        # 2. Étudiants existants
        self.etudiant1 = Etudiant.objects.create(
            matricule="ENA2025001",
            nom="KOUASSI",
            prenom="Ablan",
            annee_promo="2025"
        )
        self.etudiant2 = Etudiant.objects.create(
            matricule="ENA2025002",
            nom="MENSAH",
            prenom="Koffi",
            annee_promo="2025"
        )
        # Note : On n'insère PAS "ENA2025999" pour tester l'ignorance propre des matricules inconnus

        # 3. Template de mapping
        self.mapping = MappingTemplate.objects.create(
            nom="Template PV L1 AG",
            config_colonnes={
                "matricule_col": "Matricule",
                "blocs_ue": [
                    {
                        "ue_code": "MTH1101",
                        "moyenne_col": "Moyenne UE",
                        "statut_col": "Statut",
                        "ec_cols": [
                            {"code": "EC1", "col": "Note Math"},
                            {"code": "EC2", "col": "Note Stat"}
                        ]
                    }
                ]
            }
        )

    def create_sample_excel_file(self):
        """Crée un fichier Excel temporaire en mémoire avec 3 étudiants (2 valides, 1 matricule inconnu)."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "PV_Notes"

        # Headers
        ws.append(["Matricule", "Nom", "Prénom", "Note Math", "Note Stat", "Moyenne UE", "Statut"])

        # Ligne 1 : Etudiant 1 valide
        ws.append(["ENA2025001", "KOUASSI", "Ablan", 14.5, 16.0, 15.25, "V"])
        # Ligne 2 : Etudiant 2 valide (statut à calculer auto si non fourni ou string)
        ws.append(["ENA2025002", "MENSAH", "Koffi", "9,5", 8.0, 8.75, "NV"])
        # Ligne 3 : Matricule inconnu qui doit être rejeté/ignoré avec log explicite
        ws.append(["ENA2025999", "INCONNU", "Jean", 12.0, 10.0, 11.0, "V"])

        temp_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        wb.save(temp_file.name)
        temp_file.seek(0)
        return temp_file

    def test_clean_decimal(self):
        self.assertEqual(clean_decimal(15), Decimal("15.00"))
        self.assertEqual(clean_decimal(14.5), Decimal("14.50"))
        self.assertEqual(clean_decimal("12,75"), Decimal("12.75"))
        self.assertEqual(clean_decimal("16.2"), Decimal("16.20"))
        self.assertIsNone(clean_decimal("invalide"))
        self.assertEqual(clean_decimal(None), Decimal("0.00"))

    def test_import_staging_task(self):
        temp_excel = self.create_sample_excel_file()
        with open(temp_excel.name, "rb") as f:
            uploaded = SimpleUploadedFile("pv_test.xlsx", f.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        import_obj = ImportFichier.objects.create(
            nom_fichier="pv_test.xlsx",
            fichier=uploaded,
            utilisateur=self.user
        )

        res = process_import_staging_task(import_obj.id)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["lignes_count"], 3)

        lignes = LigneBrute.objects.filter(import_fichier=import_obj)
        self.assertEqual(lignes.count(), 3)
        self.assertEqual(lignes[0].donnees_brutes["Matricule"], "ENA2025001")
        self.assertEqual(lignes[0].statut_traitement, "en_attente")

    def test_import_validation_task_with_missing_matricule(self):
        # 1. Staging
        temp_excel = self.create_sample_excel_file()
        with open(temp_excel.name, "rb") as f:
            uploaded = SimpleUploadedFile("pv_test.xlsx", f.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        import_obj = ImportFichier.objects.create(
            nom_fichier="pv_test.xlsx",
            fichier=uploaded,
            utilisateur=self.user,
            mapping=self.mapping
        )

        process_import_staging_task(import_obj.id)

        # 2. Validation
        val_res = process_import_validation_task(import_obj.id)
        self.assertEqual(val_res["status"], "success")
        self.assertEqual(val_res["succes_count"], 2)
        self.assertEqual(val_res["rejets_count"], 1)
        self.assertIn("ENA2025999", val_res["matricules_manquants"])

        # 3. Vérification des résultats créés en base
        res_ue = ResultatUE.objects.filter(import_fichier=import_obj)
        self.assertEqual(res_ue.count(), 2)

        res_koffi = ResultatUE.objects.get(etudiant=self.etudiant2, ue=self.ue)
        self.assertEqual(res_koffi.moyenne_ue, Decimal("8.75"))
        self.assertEqual(res_koffi.statut, "NV")

        notes_koffi = NoteEC.objects.filter(etudiant=self.etudiant2)
        self.assertEqual(notes_koffi.count(), 2)
        note_math = NoteEC.objects.get(etudiant=self.etudiant2, ec=self.ec1)
        self.assertEqual(note_math.note, Decimal("9.50"))

        # 4. Vérification de la ligne rejetée
        ligne_inconnu = LigneBrute.objects.get(import_fichier=import_obj, donnees_brutes__Matricule="ENA2025999")
        self.assertEqual(ligne_inconnu.statut_traitement, "erreur")
        self.assertIn("absent de la base étudiante", ligne_inconnu.message_erreur)
