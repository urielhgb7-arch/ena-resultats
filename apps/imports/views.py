from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect

from apps.portail_admin.mixins import AdminRequiredMixin
from .models import ImportFichier
from .forms import ImportFichierForm
from .services import extraire_lignes_brutes


class ImportFichierListView(AdminRequiredMixin, ListView):
    model = ImportFichier
    template_name = "imports/import_list.html"
    context_object_name = "imports"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        statut = self.request.GET.get("statut")
        if statut:
            qs = qs.filter(statut=statut)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statut_actuel"] = self.request.GET.get("statut", "")
        return context


class ImportFichierCreateView(AdminRequiredMixin, CreateView):
    model = ImportFichier
    form_class = ImportFichierForm
    template_name = "imports/import_form.html"

    def form_valid(self, form):
        form.instance.utilisateur = self.request.user
        form.instance.nom_fichier = self.request.FILES["fichier"].name
        response = super().form_valid(form)
        
        # Extraire les lignes brutes
        try:
            lignes = extraire_lignes_brutes(self.object.fichier.path, self.object)
            messages.success(
                self.request, f"{len(lignes)} lignes détectées et prêtes pour le mapping."
            )
        except Exception as e:
            messages.error(self.request, f"Erreur lors de la lecture du fichier : {e}")
            self.object.statut = "annule"
            self.object.save()
            
        return response

    def get_success_url(self):
        return reverse_lazy("imports:detail", kwargs={"pk": self.object.pk})


class ImportFichierDetailView(AdminRequiredMixin, DetailView):
    model = ImportFichier
    template_name = "imports/import_detail.html"
    context_object_name = "import_fichier"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Limiter à 50 pour l'aperçu
        context["lignes"] = self.object.lignes.all()[:50]
        return context


class ImportFichierDeleteView(AdminRequiredMixin, DeleteView):
    model = ImportFichier
    template_name = "imports/import_confirm_delete.html"
    success_url = reverse_lazy("imports:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "L'import a été supprimé avec succès.")
        return super().delete(request, *args, **kwargs)
