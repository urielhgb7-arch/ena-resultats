from django.shortcuts import render, get_object_or_404, redirect
from .models import AnneeAcademique, Niveau, Filiere, Specialite, Semestre, SessionResultat


def accueil(request):
    annees = AnneeAcademique.objects.filter(active=True)
    return render(request, "filieres/accueil.html", {"annees": annees})


def liste_niveaux(request, annee_id):
    annee = get_object_or_404(AnneeAcademique, id=annee_id)
    niveaux = annee.niveaux.all()
    return render(
        request, "filieres/niveaux.html", {"annee": annee, "niveaux": niveaux}
    )


def liste_filieres(request, niveau_id):
    niveau = get_object_or_404(Niveau, id=niveau_id)
    filieres = niveau.filieres.all()
    return render(
        request, "filieres/filieres.html", {"niveau": niveau, "filieres": filieres}
    )


def liste_specialites(request, filiere_id):
    """
    Point d'attention : cette vue gère les 2 cas d'exception.
    - Si la filière n'a pas de spécialités (Secrétariat de Gestion) :
      on saute directement aux semestres.
    - Si la filière a une spécialité unique auto-sélectionnée (STID) :
      on saute directement aux semestres avec cette spécialité pré-choisie.
    """
    filiere = get_object_or_404(Filiere, id=filiere_id)

    if not filiere.a_des_specialites:
        return redirect("filieres:semestres", filiere_id=filiere.id)

    if filiere.specialite_unique_auto:
        specialite = filiere.specialite_par_defaut
        if specialite:
            return redirect(
                "filieres:semestres", filiere_id=filiere.id, specialite_id=specialite.id
            )

    specialites = filiere.specialites.all()
    return render(
        request,
        "filieres/specialites.html",
        {"filiere": filiere, "specialites": specialites},
    )


def liste_semestres(request, filiere_id, specialite_id=None):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    specialite = (
        get_object_or_404(Specialite, id=specialite_id) if specialite_id else None
    )
    semestres = filiere.semestres.all()
    return render(
        request,
        "filieres/semestres.html",
        {"filiere": filiere, "specialite": specialite, "semestres": semestres},
    )


def liste_sessions(request, semestre_id, specialite_id=None):
    semestre = get_object_or_404(Semestre, id=semestre_id)
    sessions = semestre.sessions.all()
    if specialite_id:
        sessions = sessions.filter(specialite_id=specialite_id)
    return render(
        request,
        "filieres/sessions.html",
        {"semestre": semestre, "sessions": sessions},
    )


def liste_ue(request, session_id):
    session = get_object_or_404(SessionResultat, id=session_id)
    ues = session.ues.filter(statut="publie")
    return render(
        request, "filieres/ue_liste.html", {"session": session, "ues": ues}
    )
