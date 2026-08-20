from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.filieres.models import SessionResultat
from .models import UE, Etudiant, ResultatUE


def detail_ue(request, ue_id):
    """
    Tableau de classement d'une UE : liste des étudiants triée par ordre
    alphabétique, avec une barre de recherche locale (par nom ou matricule).
    """
    ue = get_object_or_404(
        UE.objects.select_related("session", "session__semestre", "session__semestre__filiere"),
        id=ue_id,
        statut="publie"
    )

    resultats = (
        ue.resultats.select_related("etudiant")
        .prefetch_related("etudiant__notes_ec")
        .order_by("etudiant__nom", "etudiant__prenom")
    )

    q = request.GET.get("q", "").strip()
    if q:
        resultats = resultats.filter(
            Q(etudiant__nom__icontains=q)
            | Q(etudiant__prenom__icontains=q)
            | Q(etudiant__matricule__icontains=q)
        )

    ecs = ue.ecs.all()

    return render(
        request,
        "resultats/ue_detail.html",
        {"ue": ue, "resultats": resultats, "ecs": ecs, "q": q},
    )


def tableau_complet_session(request, session_id):
    """Affiche le tableau consolidé de toutes les UE d'une session."""
    session = get_object_or_404(
        SessionResultat.objects.select_related("semestre", "semestre__filiere"),
        id=session_id
    )
    ues = session.ues.filter(statut="publie").prefetch_related("ecs")
    
    # Tous les résultats de cette session
    resultats = ResultatUE.objects.filter(ue__in=ues).select_related("etudiant", "ue").order_by("etudiant__nom", "etudiant__prenom")

    return render(
        request,
        "resultats/session_tableau.html",
        {"session": session, "ues": ues, "resultats": resultats}
    )


def recherche_personnelle(request):
    """Recherche personnelle par nom/prénom ou matricule."""
    q = request.GET.get("q", "").strip()
    etudiants = []
    if q:
        etudiants = Etudiant.objects.filter(
            Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(matricule__icontains=q)
        ).prefetch_related("resultats_ue__ue", "notes_ec__ec")

    return render(
        request,
        "resultats/recherche.html",
        {"q": q, "etudiants": etudiants}
    )
