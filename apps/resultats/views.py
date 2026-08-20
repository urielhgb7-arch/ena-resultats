from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q, Avg, Max, Min
from apps.filieres.models import SessionResultat
from .models import UE, Etudiant, ResultatUE, NoteEC


def detail_ue(request, ue_id):
    """
    Tâche 10 : Tableau interactif de classement d'une UE.
    - Tri dynamique (par mérite / moyenne décroissante, alphabétique, etc.)
    - Recherche instantanée HTMX & Alpine.js
    - Synthèse statistique (Taux de réussite, moyenne de promo, note max/min)
    - Grille des notes d'éléments constitutifs (EC)
    """
    ue = get_object_or_404(
        UE.objects.select_related(
            "session",
            "session__semestre",
            "session__semestre__filiere",
            "session__semestre__filiere__niveau",
            "session__semestre__filiere__niveau__annee",
            "session__specialite"
        ).prefetch_related("ecs"),
        id=ue_id,
        statut="publie"
    )

    # Récupération de tous les résultats de l'UE
    queryset = ue.resultats.select_related("etudiant").prefetch_related("etudiant__notes_ec")

    # Recherche locale (Nom / Prénom / Matricule)
    q = request.GET.get("q", "").strip()
    if q:
        queryset = queryset.filter(
            Q(etudiant__nom__icontains=q)
            | Q(etudiant__prenom__icontains=q)
            | Q(etudiant__matricule__icontains=q)
        )

    # Tri dynamique
    tri = request.GET.get("tri", "nom_asc")
    if tri == "moyenne_desc":
        queryset = queryset.order_by("-moyenne_ue", "etudiant__nom", "etudiant__prenom")
    elif tri == "moyenne_asc":
        queryset = queryset.order_by("moyenne_ue", "etudiant__nom", "etudiant__prenom")
    elif tri == "matricule_asc":
        queryset = queryset.order_by("etudiant__matricule", "etudiant__nom")
    else:  # nom_asc par défaut
        queryset = queryset.order_by("etudiant__nom", "etudiant__prenom")

    resultats = list(queryset)

    # Statistiques globales de l'UE (calculées sur l'ensemble des résultats de l'UE, non filtrés)
    tous_resultats = ue.resultats.all()
    total_etudiants = tous_resultats.count()
    valides_count = tous_resultats.filter(statut__in=["V", "V*"]).count()
    taux_reussite = round((valides_count / total_etudiants) * 100, 1) if total_etudiants > 0 else 0
    stats_agg = tous_resultats.aggregate(
        moy_promo=Avg("moyenne_ue"),
        note_max=Max("moyenne_ue"),
        note_min=Min("moyenne_ue")
    )

    # Préparation des notes EC associées pour affichage rapide en template
    ecs = list(ue.ecs.all())
    
    # Mapping étudiant_id -> {ec_id: note}
    notes_map = {}
    if resultats:
        notes_qs = NoteEC.objects.filter(
            ec__in=ecs,
            etudiant_id__in=[r.etudiant_id for r in resultats]
        )
        for n in notes_qs:
            if n.etudiant_id not in notes_map:
                notes_map[n.etudiant_id] = {}
            notes_map[n.etudiant_id][n.ec_id] = n.note

    # Enrichit chaque objet résultat avec ses notes par EC et son rang
    for idx, res in enumerate(resultats, start=1):
        res.rang = idx
        res.ec_notes = [
            notes_map.get(res.etudiant_id, {}).get(ec.id, "-")
            for ec in ecs
        ]

    semestre = ue.session.semestre
    filiere = semestre.filiere

    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": filiere.niveau.annee.libelle, "url": reverse("filieres:niveaux", args=[filiere.niveau.annee.id])},
        {"label": filiere.niveau.libelle, "url": reverse("filieres:filieres", args=[filiere.niveau.id])},
        {"label": filiere.nom, "url": reverse("filieres:semestres", args=[filiere.id])},
        {"label": semestre.libelle, "url": reverse("filieres:sessions", args=[semestre.id])},
        {"label": ue.session.get_type_display(), "url": reverse("filieres:ue_liste", args=[ue.session.id])},
        {"label": f"{ue.code} - {ue.nom}", "url": request.path},
    ]

    context = {
        "ue": ue,
        "resultats": resultats,
        "ecs": ecs,
        "q": q,
        "tri": tri,
        "total_etudiants": total_etudiants,
        "valides_count": valides_count,
        "taux_reussite": taux_reussite,
        "moy_promo": round(stats_agg["moy_promo"], 2) if stats_agg["moy_promo"] else "-",
        "note_max": stats_agg["note_max"] if stats_agg["note_max"] is not None else "-",
        "note_min": stats_agg["note_min"] if stats_agg["note_min"] is not None else "-",
        "breadcrumb": breadcrumb,
    }

    # Si requête HTMX partielle : renvoie uniquement le corps du tableau
    if request.headers.get("HX-Request"):
        return render(request, "resultats/partials/ue_table_rows.html", context)

    return render(request, "resultats/ue_detail.html", context)


def tableau_complet_session(request, session_id):
    """Affiche le tableau consolidé de toutes les UE d'une session."""
    session = get_object_or_404(
        SessionResultat.objects.select_related(
            "semestre",
            "semestre__filiere",
            "semestre__filiere__niveau",
            "semestre__filiere__niveau__annee",
            "specialite"
        ),
        id=session_id
    )
    ues = session.ues.filter(statut="publie").prefetch_related("ecs")
    
    resultats = (
        ResultatUE.objects.filter(ue__in=ues)
        .select_related("etudiant", "ue")
        .order_by("etudiant__nom", "etudiant__prenom", "ue__code")
    )

    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": session.semestre.filiere.nom, "url": reverse("filieres:semestres", args=[session.semestre.filiere.id])},
        {"label": session.semestre.libelle, "url": reverse("filieres:sessions", args=[session.semestre.id])},
        {"label": f"Synthèse {session.get_type_display()}", "url": request.path},
    ]

    return render(
        request,
        "resultats/session_tableau.html",
        {"session": session, "ues": ues, "resultats": resultats, "breadcrumb": breadcrumb}
    )


def recherche_personnelle(request):
    """
    Tâche 11 : Moteur de recherche personnel.
    - Recherche instantanée par Nom / Prénom OU Matricule
    - Toggle de mode (Matricule vs Nom)
    - Relevé personnel complet regroupé par UE avec total des crédits ECTS
    """
    q = request.GET.get("q", "").strip()
    mode = request.GET.get("mode", "auto")  # 'auto', 'matricule', 'nom'

    etudiants_data = []

    if q:
        query = Q()
        if mode == "matricule":
            query = Q(matricule__iexact=q) | Q(matricule__icontains=q)
        elif mode == "nom":
            # Recherche découpée par mots (Nom et/ou Prénom)
            mots = q.split()
            for mot in mots:
                query |= Q(nom__icontains=mot) | Q(prenom__icontains=mot)
        else:  # mode 'auto'
            query = Q(matricule__icontains=q) | Q(nom__icontains=q) | Q(prenom__icontains=q)

        etudiants = (
            Etudiant.objects.filter(query)
            .prefetch_related(
                "resultats_ue__ue__session__semestre__filiere",
                "notes_ec__ec__ue"
            )
            .distinct()[:20]  # Limite à 20 résultats max pour la performance
        )

        for etu in etudiants:
            # Récupère uniquement les résultats des UE publiées
            res_publies = [
                r for r in etu.resultats_ue.all()
                if r.ue.statut == "publie"
            ]
            
            # Calcul du total des crédits ECTS validés
            credits_valides = sum(
                r.ue.credits for r in res_publies
                if r.statut in ["V", "V*"]
            )
            credits_inscrits = sum(r.ue.credits for r in res_publies)

            etudiants_data.append({
                "etudiant": etu,
                "resultats": res_publies,
                "credits_valides": credits_valides,
                "credits_inscrits": credits_inscrits,
            })

    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": "Recherche de Résultats", "url": request.path},
    ]

    context = {
        "q": q,
        "mode": mode,
        "etudiants_data": etudiants_data,
        "count": len(etudiants_data),
        "breadcrumb": breadcrumb,
    }

    # Support HTMX pour rafraîchissement instantané
    if request.headers.get("HX-Request"):
        return render(request, "resultats/partials/recherche_results.html", context)

    return render(request, "resultats/recherche.html", context)
