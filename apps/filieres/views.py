from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import AnneeAcademique, Niveau, Filiere, Specialite, Semestre, SessionResultat


def accueil(request):
    """Page d'accueil : affiche l'année active par défaut et les années disponibles."""
    annee_active = AnneeAcademique.objects.filter(active=True).first()
    toutes_annees = AnneeAcademique.objects.all().order_by("-libelle")
    niveaux_actifs = annee_active.niveaux.all() if annee_active else []

    context = {
        "annee_active": annee_active,
        "annees": toutes_annees,
        "niveaux_actifs": niveaux_actifs,
        "breadcrumb": [{"label": "Accueil", "url": reverse("filieres:accueil")}],
    }
    return render(request, "filieres/accueil.html", context)


def liste_niveaux(request, annee_id):
    annee = get_object_or_404(AnneeAcademique, id=annee_id)
    niveaux = annee.niveaux.all()
    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": annee.libelle, "url": reverse("filieres:niveaux", args=[annee.id])},
    ]
    context = {"annee": annee, "niveaux": niveaux, "breadcrumb": breadcrumb}
    return render(request, "filieres/niveaux.html", context)


def liste_filieres(request, niveau_id):
    niveau = get_object_or_404(Niveau.objects.select_related("annee"), id=niveau_id)
    filieres = niveau.filieres.all()
    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": niveau.annee.libelle, "url": reverse("filieres:niveaux", args=[niveau.annee.id])},
        {"label": niveau.libelle, "url": reverse("filieres:filieres", args=[niveau.id])},
    ]
    context = {"niveau": niveau, "filieres": filieres, "breadcrumb": breadcrumb}
    return render(request, "filieres/filieres.html", context)


def liste_specialites(request, filiere_id):
    """
    Règle métier ENA :
    - Si la filière n'a pas de spécialités (ex: Secrétariat de Gestion) : saut direct aux semestres.
    - Si la filière a une spécialité unique auto-sélectionnée (ex: STID) : saut direct avec spécialité pré-choisie.
    """
    filiere = get_object_or_404(
        Filiere.objects.select_related("niveau", "niveau__annee"), id=filiere_id
    )

    if not filiere.a_des_specialites:
        return redirect("filieres:semestres", filiere_id=filiere.id)

    if filiere.specialite_unique_auto:
        specialite = filiere.specialite_par_defaut
        if specialite:
            return redirect(
                "filieres:semestres_avec_specialite",
                filiere_id=filiere.id,
                specialite_id=specialite.id,
            )

    specialites = filiere.specialites.all()
    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": filiere.niveau.annee.libelle, "url": reverse("filieres:niveaux", args=[filiere.niveau.annee.id])},
        {"label": filiere.niveau.libelle, "url": reverse("filieres:filieres", args=[filiere.niveau.id])},
        {"label": filiere.nom, "url": reverse("filieres:specialites", args=[filiere.id])},
    ]
    context = {
        "filiere": filiere,
        "specialites": specialites,
        "breadcrumb": breadcrumb,
    }
    return render(request, "filieres/specialites.html", context)


def liste_semestres(request, filiere_id, specialite_id=None):
    filiere = get_object_or_404(
        Filiere.objects.select_related("niveau", "niveau__annee"), id=filiere_id
    )
    specialite = (
        get_object_or_404(Specialite, id=specialite_id, filiere=filiere)
        if specialite_id
        else None
    )
    semestres = filiere.semestres.all()

    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": filiere.niveau.annee.libelle, "url": reverse("filieres:niveaux", args=[filiere.niveau.annee.id])},
        {"label": filiere.niveau.libelle, "url": reverse("filieres:filieres", args=[filiere.niveau.id])},
        {"label": filiere.nom, "url": reverse("filieres:specialites" if filiere.a_des_specialites else "filieres:semestres", args=[filiere.id])},
    ]
    if specialite:
        breadcrumb.append({"label": specialite.nom, "url": request.path})
    breadcrumb.append({"label": "Semestres", "url": request.path})

    context = {
        "filiere": filiere,
        "specialite": specialite,
        "semestres": semestres,
        "breadcrumb": breadcrumb,
    }
    return render(request, "filieres/semestres.html", context)


def liste_sessions(request, semestre_id, specialite_id=None):
    semestre = get_object_or_404(
        Semestre.objects.select_related("filiere", "filiere__niveau", "filiere__niveau__annee"),
        id=semestre_id
    )
    specialite = (
        get_object_or_404(Specialite, id=specialite_id, filiere=semestre.filiere)
        if specialite_id
        else None
    )
    sessions = semestre.sessions.all()
    if specialite:
        sessions = sessions.filter(specialite=specialite)

    filiere = semestre.filiere
    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": filiere.niveau.annee.libelle, "url": reverse("filieres:niveaux", args=[filiere.niveau.annee.id])},
        {"label": filiere.niveau.libelle, "url": reverse("filieres:filieres", args=[filiere.niveau.id])},
        {"label": filiere.nom, "url": reverse("filieres:semestres", args=[filiere.id])},
        {"label": semestre.libelle, "url": request.path},
        {"label": "Sessions", "url": request.path},
    ]

    context = {
        "semestre": semestre,
        "specialite": specialite,
        "sessions": sessions,
        "breadcrumb": breadcrumb,
    }
    return render(request, "filieres/sessions.html", context)


def liste_ue(request, session_id):
    """Affiche les Unités d'Enseignement publiées pour une session donnée."""
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
    # Seules les UE au statut 'publie' sont visibles au public
    ues = session.ues.filter(statut="publie").prefetch_related("ecs")

    semestre = session.semestre
    filiere = semestre.filiere

    breadcrumb = [
        {"label": "Accueil", "url": reverse("filieres:accueil")},
        {"label": filiere.niveau.annee.libelle, "url": reverse("filieres:niveaux", args=[filiere.niveau.annee.id])},
        {"label": filiere.niveau.libelle, "url": reverse("filieres:filieres", args=[filiere.niveau.id])},
        {"label": filiere.nom, "url": reverse("filieres:semestres", args=[filiere.id])},
        {"label": semestre.libelle, "url": reverse("filieres:sessions", args=[semestre.id])},
        {"label": session.get_type_display(), "url": request.path},
        {"label": "Unités d'Enseignement", "url": request.path},
    ]

    context = {
        "session": session,
        "ues": ues,
        "breadcrumb": breadcrumb,
    }
    return render(request, "filieres/ue_liste.html", context)
