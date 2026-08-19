from django.contrib import admin
from .models import UE, EC, Etudiant, NoteEC, ResultatUE

@admin.register(UE)
class UEAdmin(admin.ModelAdmin):
    list_display = ("code", "nom", "session", "credits", "statut", "date_publication")
    list_filter = ("statut", "session")
    search_fields = ("code", "nom")


@admin.register(EC)
class ECAdmin(admin.ModelAdmin):
    list_display = ("code", "nom", "ue")
    list_filter = ("ue",)
    search_fields = ("code", "nom")


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ("matricule", "nom", "prenom", "annee_promo")
    list_filter = ("annee_promo",)
    search_fields = ("matricule", "nom", "prenom")


@admin.register(NoteEC)
class NoteECAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "ec", "note", "import_fichier")
    list_filter = ("ec__ue",)
    search_fields = ("etudiant__matricule", "etudiant__nom", "etudiant__prenom")
    autocomplete_fields = ["etudiant", "ec", "import_fichier"]


@admin.register(ResultatUE)
class ResultatUEAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "ue", "moyenne_ue", "statut", "import_fichier")
    list_filter = ("statut", "ue")
    search_fields = ("etudiant__matricule", "etudiant__nom", "etudiant__prenom")
    autocomplete_fields = ["etudiant", "ue", "import_fichier"]
