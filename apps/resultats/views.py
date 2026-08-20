from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q, Avg, Max, Min
from apps.filieres.models import AnneeAcademique, Niveau, Filiere, Semestre, SessionResultat
from .models import UE, Etudiant, ResultatUE, NoteEC


def detail_ue(request, ue_id):
    """
    Tâche 10 : Tableau interactif de classement d'une UE.
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

    queryset = ue.resultats.select_related("etudiant").prefetch_related("etudiant__notes_ec")

    q = request.GET.get("q", "").strip()
    if q:
        queryset = queryset.filter(
            Q(etudiant__nom__icontains=q)
            | Q(etudiant__prenom__icontains=q)
            | Q(etudiant__matricule__icontains=q)
        )

    tri = request.GET.get("tri", "nom_asc")
    if tri == "moyenne_desc":
        queryset = queryset.order_by("-moyenne_ue", "etudiant__nom", "etudiant__prenom")
    elif tri == "moyenne_asc":
        queryset = queryset.order_by("moyenne_ue", "etudiant__nom", "etudiant__prenom")
    elif tri == "matricule_asc":
        queryset = queryset.order_by("etudiant__matricule", "etudiant__nom")
    else:
        queryset = queryset.order_by("etudiant__nom", "etudiant__prenom")

    resultats = list(queryset)

    tous_resultats = ue.resultats.all()
    total_etudiants = tous_resultats.count()
    valides_count = tous_resultats.filter(statut__in=["V", "V*"]).count()
    taux_reussite = round((valides_count / total_etudiants) * 100, 1) if total_etudiants > 0 else 0
    stats_agg = tous_resultats.aggregate(
        moy_promo=Avg("moyenne_ue"),
        note_max=Max("moyenne_ue"),
        note_min=Min("moyenne_ue")
    )

    ecs = list(ue.ecs.all())
    
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
    Tâches 11 & 12 : Consultation des notes d'un étudiant de L1 à L3 (sans relevé PDF formel).
    - Regroupement des notes par Niveau (Licence 1, 2, 3) et par Semestre (S1 à S6).
    - Calcul des crédits ECTS validés par semestre et sur tout le cursus.
    - Recherche par Nom/Prénom ou Matricule avec sélecteur de mode.
    """
    q = request.GET.get("q", "").strip()
    mode = request.GET.get("mode", "auto")

    etudiants_data = []

    if q:
        query = Q()
        if mode == "matricule":
            query = Q(matricule__iexact=q) | Q(matricule__icontains=q)
        elif mode == "nom":
            mots = q.split()
            for mot in mots:
                query |= Q(nom__icontains=mot) | Q(prenom__icontains=mot)
        else:
            query = Q(matricule__icontains=q) | Q(nom__icontains=q) | Q(prenom__icontains=q)

        etudiants = (
            Etudiant.objects.filter(query)
            .prefetch_related(
                "resultats_ue__ue__session__semestre__filiere__niveau__annee",
                "resultats_ue__ue__ecs",
                "notes_ec__ec__ue"
            )
            .distinct()[:20]
        )

        for etu in etudiants:
            # Récupère tous les résultats des UE publiées
            res_publies = [
                r for r in etu.resultats_ue.all()
                if r.ue.statut == "publie"
            ]

            # Organisation hiérarchique par Niveau (L1, L2, L3) puis par Semestre (S1, S2...)
            niveaux_tree = {}
            total_credits_valides = 0
            total_credits_inscrits = 0
            filiere_nom = ""

            for r in res_publies:
                session = r.ue.session
                semestre = session.semestre
                filiere = semestre.filiere
                niveau = filiere.niveau

                if not filiere_nom:
                    filiere_nom = filiere.nom

                niv_code = niveau.libelle if niveau else "Cycle"
                sem_libelle = semestre.libelle

                if niv_code not in niveaux_tree:
                    niveaux_tree[niv_code] = {
                        "libelle": f"Licence {niv_code[1:]}" if niv_code.startswith("L") else niv_code,
                        "semestres": {}
                    }

                if sem_libelle not in niveaux_tree[niv_code]["semestres"]:
                    niveaux_tree[niv_code]["semestres"][sem_libelle] = {
                        "libelle": sem_libelle,
                        "filiere": filiere.nom,
                        "ues": [],
                        "credits_valides": 0,
                        "credits_totaux": 0
                    }

                is_valide = r.statut in ["V", "V*"]
                if is_valide:
                    niveaux_tree[niv_code]["semestres"][sem_libelle]["credits_valides"] += r.ue.credits
                    total_credits_valides += r.ue.credits

                niveaux_tree[niv_code]["semestres"][sem_libelle]["credits_totaux"] += r.ue.credits
                total_credits_inscrits += r.ue.credits

                niveaux_tree[niv_code]["semestres"][sem_libelle]["ues"].append(r)

            etudiants_data.append({
                "etudiant": etu,
                "filiere_nom": filiere_nom,
                "niveaux_tree": niveaux_tree,
                "credits_valides": total_credits_valides,
                "credits_inscrits": total_credits_inscrits,
            })

    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": "Consultation des Notes L1-L3", "url": request.path},
    ]

    context = {
        "q": q,
        "mode": mode,
        "etudiants_data": etudiants_data,
        "count": len(etudiants_data),
        "breadcrumb": breadcrumb,
    }

    if request.headers.get("HX-Request"):
        return render(request, "resultats/partials/recherche_results.html", context)

    return render(request, "resultats/recherche.html", context)


def recherche_avancee(request):
    """
    Tâche 13 : Recherche directe / avancée avec filtres en cascade.
    Permet à l'étudiant de choisir Année -> Niveau -> Filière -> Semestre
    et d'accéder directement aux procès-verbaux d'évaluation.
    """
    annee_id = request.GET.get("annee_id")
    niveau_id = request.GET.get("niveau_id")
    filiere_id = request.GET.get("filiere_id")
    semestre_id = request.GET.get("semestre_id")

    # Si le formulaire complet est soumis, redirection vers la vue correspondante
    if filiere_id:
        if semestre_id:
            return redirect("filieres:sessions", semestre_id=semestre_id)
        return redirect("filieres:semestres", filiere_id=filiere_id)

    annees = AnneeAcademique.objects.all().order_by("-libelle")

    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": "Recherche Directe", "url": request.path},
    ]

    context = {
        "annees": annees,
        "breadcrumb": breadcrumb,
    }
    return render(request, "resultats/recherche_avancee.html", context)
