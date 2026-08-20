from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
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


# --- Endpoints AJAX / HTMX pour la recherche en cascade (Tâche 13) ---

def ajax_niveaux(request):
    annee_id = request.GET.get("annee_id")
    options = ['<option value="">— Choisir un niveau —</option>']
    if annee_id:
        niveaux = Niveau.objects.filter(annee_id=annee_id)
        for n in niveaux:
            options.append(f'<option value="{n.id}">{n.libelle}</option>')
    return HttpResponse("\n".join(options))


def ajax_filieres(request):
    niveau_id = request.GET.get("niveau_id")
    options = ['<option value="">— Choisir une filière —</option>']
    if niveau_id:
        filieres = Filiere.objects.filter(niveau_id=niveau_id)
        for f in filieres:
            options.append(f'<option value="{f.id}">{f.nom}</option>')
    return HttpResponse("\n".join(options))


def ajax_semestres(request):
    filiere_id = request.GET.get("filiere_id")
    options = ['<option value="">Tous les semestres</option>']
    if filiere_id:
        semestres = Semestre.objects.filter(filiere_id=filiere_id)
        for s in semestres:
            options.append(f'<option value="{s.id}">{s.libelle}</option>')
    return HttpResponse("\n".join(options))


# --- ADMIN CBVs ---
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from apps.portail_admin.mixins import AdminRequiredMixin
from .forms import FiliereForm

class FiliereListView(AdminRequiredMixin, ListView):
    model = Filiere
    template_name = "filieres/filiere_list.html"
    context_object_name = "filieres"
    paginate_by = 20
    
    def get_queryset(self):
        return Filiere.objects.select_related('niveau__annee').all()

class FiliereCreateView(AdminRequiredMixin, CreateView):
    model = Filiere
    form_class = FiliereForm
    template_name = "filieres/filiere_form.html"
    success_url = reverse_lazy("filieres:list")

    def form_valid(self, form):
        messages.success(self.request, "La filière a été créée avec succès.")
        return super().form_valid(form)

class FiliereUpdateView(AdminRequiredMixin, UpdateView):
    model = Filiere
    form_class = FiliereForm
    template_name = "filieres/filiere_form.html"
    success_url = reverse_lazy("filieres:list")

    def form_valid(self, form):
        messages.success(self.request, "La filière a été mise à jour avec succès.")
        return super().form_valid(form)

class FiliereDeleteView(AdminRequiredMixin, DeleteView):
    model = Filiere
    template_name = "filieres/filiere_confirm_delete.html"
    success_url = reverse_lazy("filieres:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "La filière a été supprimée avec succès.")
        return super().delete(request, *args, **kwargs)
