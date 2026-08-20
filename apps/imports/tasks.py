import logging
from decimal import Decimal, InvalidOperation
from django.db import transaction
import openpyxl

from apps.imports.models import ImportFichier, LigneBrute, MappingTemplate
from apps.resultats.models import Etudiant, UE, EC, ResultatUE, NoteEC

logger = logging.getLogger(__name__)


def clean_decimal(value):
    """Convertit une valeur brute Excel en Decimal propre pour les notes et moyennes."""
    if value is None:
        return Decimal("0.00")
    if isinstance(value, (int, float)):
        return Decimal(str(round(value, 2)))
    if isinstance(value, str):
        # Remplace virgule par point
        clean_str = value.replace(",", ".").strip()
        try:
            return Decimal(clean_str)
        except InvalidOperation:
            return None
    return None


def process_import_staging_task(import_fichier_id):
    """
    Tâche Asynchrone (Tâche 6) :
    Lit le fichier Excel .xlsx téléversé et génère toutes les LigneBrute par lot en base (Zero timeout).
    """
    try:
        import_obj = ImportFichier.objects.get(pk=import_fichier_id)
        if not import_obj.fichier:
            return {"status": "error", "message": "Aucun fichier attaché."}

        wb = openpyxl.load_workbook(import_obj.fichier.path, data_only=True)
        sheet = wb.active

        rows = list(sheet.iter_rows(values_only=True))
        if not rows or len(rows) <= 1:
            return {"status": "error", "message": "Fichier Excel vide ou sans en-tête."}

        headers = [str(h).strip() if h is not None else f"col_{idx}" for idx, h in enumerate(rows[0])]

        lignes_brutes = []
        for row_idx, row in enumerate(rows[1:], start=2):
            donnees = {}
            has_data = False
            for col_idx, val in enumerate(row):
                if val is not None and str(val).strip() != "":
                    has_data = True
                    if isinstance(val, (int, float, bool)):
                        donnees[headers[col_idx]] = val
                    else:
                        donnees[headers[col_idx]] = str(val).strip()
                else:
                    donnees[headers[col_idx]] = None

            if has_data:
                lignes_brutes.append(
                    LigneBrute(
                        import_fichier=import_obj,
                        numero_ligne=row_idx,
                        donnees_brutes=donnees,
                        statut_traitement="en_attente"
                    )
                )

        if lignes_brutes:
            with transaction.atomic():
                # Nettoie les anciennes lignes si ré-import
                LigneBrute.objects.filter(import_fichier=import_obj).delete()
                LigneBrute.objects.bulk_create(lignes_brutes, batch_size=500)

            import_obj.statut = "en_attente"
            import_obj.save(update_fields=["statut"])

        logger.info(f"Import {import_fichier_id} mis en staging avec succès ({len(lignes_brutes)} lignes).")
        return {
            "status": "success",
            "lignes_count": len(lignes_brutes),
            "headers": headers
        }

    except Exception as exc:
        logger.exception(f"Erreur lors du staging de l'import {import_fichier_id}: {exc}")
        return {"status": "error", "message": str(exc)}


def process_import_validation_task(import_fichier_id, mapping_id=None):
    """
    Tâche Asynchrone (Tâches 7 & 8) :
    Applique le template de mapping sur les LigneBrute, valide les données,
    ignore les matricules absents en traçant l'erreur sur LigneBrute,
    et insère en masse (bulk) ResultatUE et NoteEC.
    """
    try:
        import_obj = ImportFichier.objects.select_related("mapping").get(pk=import_fichier_id)
        
        mapping_obj = None
        if mapping_id:
            mapping_obj = MappingTemplate.objects.get(pk=mapping_id)
            import_obj.mapping = mapping_obj
            import_obj.save(update_fields=["mapping"])
        else:
            mapping_obj = import_obj.mapping

        if not mapping_obj:
            return {"status": "error", "message": "Aucun mapping template associé à cet import."}

        config = mapping_obj.config_colonnes
        matricule_col = config.get("matricule_col", "Matricule")
        blocs_ue = config.get("blocs_ue", [])

        # Si le mapping est au format simplifié plat (une seule UE)
        if not blocs_ue and ("ue_id" in config or "ue_code" in config):
            blocs_ue = [
                {
                    "ue_id": config.get("ue_id"),
                    "ue_code": config.get("ue_code"),
                    "moyenne_col": config.get("moyenne_col"),
                    "statut_col": config.get("statut_col"),
                    "ec_cols": config.get("ec_cols", [])
                }
            ]

        lignes_brutes = list(LigneBrute.objects.filter(import_fichier=import_obj))
        if not lignes_brutes:
            return {"status": "error", "message": "Aucune ligne brute à traiter."}

        # 1. Extraction de tous les matricules du fichier
        matricules_fichier = set()
        for ligne in lignes_brutes:
            mat = ligne.donnees_brutes.get(matricule_col)
            if mat:
                matricules_fichier.add(str(mat).strip())

        # 2. Requête par lot (Bulk Select) : Chargement de tous les étudiants concernés en 1 requête SQL
        etudiants = Etudiant.objects.filter(matricule__in=matricules_fichier)
        etudiants_map = {e.matricule.strip(): e for e in etudiants if e.matricule}

        # 3. Pré-chargement des UEs et ECs concernés
        ue_ids = [b.get("ue_id") for b in blocs_ue if b.get("ue_id")]
        ue_codes = [b.get("ue_code") for b in blocs_ue if b.get("ue_code")]
        
        ues_queryset = UE.objects.filter(id__in=ue_ids) | UE.objects.filter(code__in=ue_codes)
        
        ues_by_id = {u.id: u for u in ues_queryset}
        ues_by_code = {u.code: u for u in ues_queryset}

        # Récupération de tous les ECs
        ec_ids = []
        for bloc in blocs_ue:
            for ec_c in bloc.get("ec_cols", []):
                if ec_c.get("ec_id"):
                    ec_ids.append(ec_c["ec_id"])
        ecs_by_id = {ec.id: ec for ec in EC.objects.filter(id__in=ec_ids)} if ec_ids else {}

        # 4. Parcours et validation ligne par ligne
        resultats_ue_to_create = []
        notes_ec_to_create = []
        succes_count = 0
        rejets_count = 0
        matricules_manquants = []

        for ligne in lignes_brutes:
            raw_mat = ligne.donnees_brutes.get(matricule_col)
            mat_str = str(raw_mat).strip() if raw_mat is not None else ""

            if not mat_str or mat_str not in etudiants_map:
                ligne.statut_traitement = "erreur"
                motif = f"Matricule '{mat_str}' absent de la base étudiante." if mat_str else "Matricule non renseigné."
                ligne.message_erreur = motif
                rejets_count += 1
                if mat_str:
                    matricules_manquants.append(mat_str)
                continue

            etudiant = etudiants_map[mat_str]
            ligne_valide = True

            # Traitement de chaque bloc UE pour cet étudiant
            for bloc in blocs_ue:
                ue_obj = None
                if bloc.get("ue_id"):
                    ue_obj = ues_by_id.get(bloc["ue_id"])
                elif bloc.get("ue_code"):
                    ue_obj = ues_by_code.get(bloc["ue_code"])

                if not ue_obj:
                    ligne.statut_traitement = "erreur"
                    ligne.message_erreur = f"UE '{bloc.get('ue_code') or bloc.get('ue_id')}' introuvable en base."
                    ligne_valide = False
                    break

                # Récupération moyenne UE
                moy_raw = ligne.donnees_brutes.get(bloc.get("moyenne_col"))
                moyenne = clean_decimal(moy_raw)

                if moyenne is None:
                    ligne.statut_traitement = "erreur"
                    ligne.message_erreur = f"Moyenne UE invalide ({moy_raw}) à la ligne {ligne.numero_ligne}."
                    ligne_valide = False
                    break

                # Statut UE
                statut_raw = ligne.donnees_brutes.get(bloc.get("statut_col"))
                if statut_raw and str(statut_raw).strip() in ["V", "NV", "V*"]:
                    statut = str(statut_raw).strip()
                else:
                    statut = "V" if moyenne >= Decimal("10.00") else "NV"

                resultats_ue_to_create.append(
                    ResultatUE(
                        etudiant=etudiant,
                        ue=ue_obj,
                        import_fichier=import_obj,
                        moyenne_ue=moyenne,
                        statut=statut
                    )
                )

                # Récupération des notes EC
                for ec_col in bloc.get("ec_cols", []):
                    ec_obj = None
                    if ec_col.get("ec_id"):
                        ec_obj = ecs_by_id.get(ec_col["ec_id"])
                    elif ec_col.get("code"):
                        ec_obj = EC.objects.filter(ue=ue_obj, code=ec_col["code"]).first()

                    if ec_obj:
                        note_raw = ligne.donnees_brutes.get(ec_col.get("col"))
                        note_dec = clean_decimal(note_raw)
                        if note_dec is not None:
                            notes_ec_to_create.append(
                                NoteEC(
                                    etudiant=etudiant,
                                    ec=ec_obj,
                                    import_fichier=import_obj,
                                    note=note_dec
                                )
                            )

            if ligne_valide:
                ligne.statut_traitement = "traite"
                ligne.message_erreur = ""
                succes_count += 1
            else:
                rejets_count += 1

        # 5. Persistance en base atomique (Bulk Create & Bulk Update)
        with transaction.atomic():
            # Supprime les anciens résultats liés à cet import en cas de re-jeu
            ResultatUE.objects.filter(import_fichier=import_obj).delete()
            NoteEC.objects.filter(import_fichier=import_obj).delete()

            if resultats_ue_to_create:
                ResultatUE.objects.bulk_create(
                    resultats_ue_to_create,
                    batch_size=500,
                    update_conflicts=True,
                    update_fields=["moyenne_ue", "statut", "import_fichier"],
                    unique_fields=["etudiant", "ue"]
                )

            if notes_ec_to_create:
                NoteEC.objects.bulk_create(
                    notes_ec_to_create,
                    batch_size=500,
                    update_conflicts=True,
                    update_fields=["note", "import_fichier"],
                    unique_fields=["etudiant", "ec"]
                )

            LigneBrute.objects.bulk_update(
                lignes_brutes,
                fields=["statut_traitement", "message_erreur"],
                batch_size=500
            )

            import_obj.statut = "applique" if rejets_count == 0 else "valide"
            import_obj.save(update_fields=["statut"])

        logger.info(
            f"Import {import_fichier_id} validé et appliqué : {succes_count} succès, {rejets_count} rejets."
        )

        return {
            "status": "success",
            "succes_count": succes_count,
            "rejets_count": rejets_count,
            "matricules_manquants": list(set(matricules_manquants))
        }

    except Exception as exc:
        logger.exception(f"Erreur lors de la validation de l'import {import_fichier_id}: {exc}")
        return {"status": "error", "message": str(exc)}
