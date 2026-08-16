from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ImportFichier
from .services import extraire_lignes_brutes


@staff_member_required
def upload_fichier(request):
    """Étape 1 : upload du fichier Excel + extraction en LigneBrute."""
    if request.method == "POST" and request.FILES.get("fichier"):
        fichier = request.FILES["fichier"]
        import_fichier = ImportFichier.objects.create(
            nom_fichier=fichier.name,
            fichier=fichier,
            utilisateur=request.user,
        )
        try:
            lignes = extraire_lignes_brutes(import_fichier.fichier.path, import_fichier)
            messages.success(
                request, f"{len(lignes)} lignes détectées et prêtes pour le mapping."
            )
        except Exception as e:
            messages.error(request, f"Erreur lors de la lecture du fichier : {e}")
            import_fichier.statut = "annule"
            import_fichier.save()
        return redirect("imports:apercu", import_id=import_fichier.id)

    return render(request, "imports/upload.html")


@staff_member_required
def apercu_import(request, import_id):
    """Étape 2 : aperçu des lignes brutes avant mapping/validation."""
    import_fichier = get_object_or_404(ImportFichier, id=import_id)
    lignes = import_fichier.lignes.all()[:50]  # aperçu limité, pas tout afficher
    return render(
        request,
        "imports/apercu.html",
        {"import_fichier": import_fichier, "lignes": lignes},
    )
