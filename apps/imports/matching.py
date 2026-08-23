"""
apps/imports/matching.py

Moteur de correspondance floue (fuzzy matching) pour identifier
automatiquement à quelle filière/UE appartient un bloc de données
détecté dans un fichier Excel multi-filières.
"""

from dataclasses import dataclass, field
from rapidfuzz import fuzz, process


SEUIL_CONFIANCE_AUTO = 85  # en dessous : jamais d'auto-classement


# Référentiel officiel (cahier des charges §4) - à terme, lire depuis la
# base (table Filiere/Specialite) plutôt que codé en dur ici. Conservé en
# dur pour ce module de test/démonstration.
REFERENTIEL_FILIERES = {
    "Administration des Finances": [
        "Administration des Impôts",
        "Administration des Finances et du Trésor",
        "Gestion des Marchés Publics",
        "Administration Hospitalière Universitaire et Intendance",
    ],
    "Administration Générale": [
        "Administration Territoriale et de Sécurité Sociale",
        "Diplomatie et Relations Internationales",
        "AGT",
    ],
    "Sciences Techniques et d'Information Documentaire": [
        "Archivistique, Bibliothéconomie et Documentation (BIDOC)",
    ],
    "Secrétariat de Gestion": [],
}


@dataclass
class SuggestionMatch:
    nom: str
    score: float


@dataclass
class ResultatMatching:
    entree: str
    statut: str  # "auto" ou "a_valider"
    candidat: str | None
    score: float
    suggestions: list[SuggestionMatch] = field(default_factory=list)


def _normaliser(texte: str) -> str:
    """Nettoyage minimal avant comparaison : espaces, casse."""
    return " ".join(texte.strip().split()).lower()


def matcher_filiere(nom_detecte: str, seuil: int = SEUIL_CONFIANCE_AUTO) -> ResultatMatching:
    """
    Compare un nom de filière détecté (ex: nom d'une feuille Excel, ou
    une ligne d'en-tête "FILIERE: ...") contre le référentiel officiel.
    """
    noms_officiels = list(REFERENTIEL_FILIERES.keys())

    resultats = process.extract(
        nom_detecte,
        noms_officiels,
        scorer=fuzz.WRatio,
        limit=3,
        processor=_normaliser,
    )

    suggestions = [SuggestionMatch(nom=r[0], score=r[1]) for r in resultats]

    if not suggestions:
        return ResultatMatching(
            entree=nom_detecte, statut="a_valider", candidat=None, score=0, suggestions=[]
        )

    meilleur = suggestions[0]

    if meilleur.score >= seuil:
        return ResultatMatching(
            entree=nom_detecte,
            statut="auto",
            candidat=meilleur.nom,
            score=meilleur.score,
            suggestions=suggestions,
        )

    return ResultatMatching(
        entree=nom_detecte,
        statut="a_valider",
        candidat=None,
        score=meilleur.score,
        suggestions=suggestions,
    )


def _normaliser_code(code: str) -> str:
    """Normalisation stricte d'un code : espaces/tirets retirés, majuscules."""
    return code.strip().upper().replace(" ", "").replace("-", "")


def matcher_ue_existante(code_detecte: str, codes_ue_existants: list[str],
                          seuil: int = SEUIL_CONFIANCE_AUTO) -> ResultatMatching:
    """
    Compare un code d'UE détecté contre les codes déjà existants dans la
    session cible.
    """
    if not codes_ue_existants:
        return ResultatMatching(
            entree=code_detecte, statut="a_valider", candidat=None, score=0, suggestions=[]
        )

    code_norm = _normaliser_code(code_detecte)
    for code_existant in codes_ue_existants:
        if _normaliser_code(code_existant) == code_norm:
            return ResultatMatching(
                entree=code_detecte,
                statut="auto",
                candidat=code_existant,
                score=100,
                suggestions=[SuggestionMatch(nom=code_existant, score=100)],
            )

    resultats = process.extract(
        code_detecte, codes_ue_existants, scorer=fuzz.ratio, limit=3
    )
    suggestions = [SuggestionMatch(nom=r[0], score=r[1]) for r in resultats]

    return ResultatMatching(
        entree=code_detecte,
        statut="a_valider",
        candidat=None,
        score=suggestions[0].score if suggestions else 0,
        suggestions=suggestions,
    )
