from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import UE


def detail_ue(request, ue_id):
    """
    Tableau de classement d'une UE : liste des étudiants triée par ordre
    alphabétique, avec une barre de recherche locale (par nom) pour
    sauter directement à sa ligne - conforme à la NB du cahier des charges.
    """
    ue = get_object_or_404(UE, id=ue_id, statut="publie")

    resultats = (
        ue.resultats.select_related("etudiant")
        .prefetch_related("etudiant__notes_ec")
        .order_by("etudiant__nom", "etudiant__prenom")
    )

    q = request.GET.get("q", "").strip()
    if q:
        resultats = resultats.filter(
            Q(etudiant__nom__icontains=q) | Q(etudiant__prenom__icontains=q)
        )

    ecs = ue.ecs.all()  # colonnes EC à afficher dans l'en-tête du tableau

    return render(
        request,
        "resultats/ue_detail.html",
        {"ue": ue, "resultats": resultats, "ecs": ecs, "q": q},
    )
