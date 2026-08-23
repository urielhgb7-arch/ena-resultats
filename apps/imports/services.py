"""
Logique de parsing du fichier Excel source.
Séparée des vues (views.py) pour rester testable sans requête HTTP.

Étape 1 (ce fichier) : lire le fichier Excel "large" (colonnes fusionnées
par UE) et le convertir en lignes brutes stockées telles quelles.
Étape 2 (mapping, à faire une fois le format réel confirmé) : transformer
les LigneBrute en NoteEC / ResultatUE en s'appuyant sur un MappingTemplate.
"""

import openpyxl
from .models import LigneBrute, ImportFichier
from .matching import matcher_filiere

def extraire_lignes_brutes(fichier_path, import_fichier: ImportFichier):
    """
    Lit un fichier Excel au format 'large' (en-têtes fusionnés par UE) et crée une LigneBrute par étudiant.
    Parcourt TOUTES les feuilles du classeur pour le support des imports globaux.
    """
    wb = openpyxl.load_workbook(fichier_path, data_only=True)
    
    mapping = import_fichier.mapping
    config = mapping.config_colonnes if mapping else {}
    col_numero = config.get("numero_col", 1) - 1
    col_matricule = config.get("matricule_col", 2) - 1
    col_nom = config.get("nom_prenoms_col", 3) - 1
    min_row = config.get("data_start_row", 3)
    ec_row = config.get("ec_row", 2)

    lignes_creees = []
    ligne_num = 0

    for ws in wb.worksheets:
        # Matcher la filière basée sur le nom de la feuille
        match_result = matcher_filiere(ws.title)
        match_info = {
            "entree": match_result.entree,
            "statut": match_result.statut,
            "candidat": match_result.candidat,
            "score": match_result.score,
        }

        # Reconstitue quelle colonne appartient à quelle UE, via les cellules fusionnées
        ue_par_colonne = {}
        for merged_range in ws.merged_cells.ranges:
            valeur = ws.cell(merged_range.min_row, merged_range.min_col).value
            if valeur and "UE" in str(valeur).upper():
                for col in range(merged_range.min_col, merged_range.max_col + 1):
                    ue_par_colonne[col] = str(valeur).replace("UE:", "").strip()

        for row in ws.iter_rows(min_row=min_row, values_only=False):
            if row[0].value is None:  # ligne vide = fin du tableau
                continue
            ligne_num += 1

            donnees = {
                "feuille_source": ws.title,
                "match_filiere": match_info,
                "numero": row[col_numero].value if col_numero < len(row) else None,
                "matricule": row[col_matricule].value if col_matricule < len(row) else None,
                "nom_prenoms": row[col_nom].value if col_nom < len(row) else None,
                "resultats_par_ue": {},
            }

            for col_idx, cell in enumerate(row, start=1):
                if col_idx in ue_par_colonne:
                    type_champ = ws.cell(ec_row, col_idx).value  # EC1, EC2, Moy UE, R
                    ue_code = ue_par_colonne[col_idx]
                    donnees["resultats_par_ue"].setdefault(ue_code, {})
                    donnees["resultats_par_ue"][ue_code][str(type_champ)] = cell.value

            ligne = LigneBrute.objects.create(
                import_fichier=import_fichier,
                numero_ligne=ligne_num,
                donnees_brutes=donnees,
            )
            lignes_creees.append(ligne)

    return lignes_creees
