from django.contrib import admin
from .models import UE, EC, Etudiant, NoteEC, ResultatUE


class ECInline(admin.TabularInline):
    model = EC
    extra = 1


@admin.register(UE)
class UEAdmin(admin.ModelAdmin):
    list_display = ("code", "nom", "credits", "session", "statut", "date_publication")
    list_filter = ("statut", "session__semestre__filiere")
    search_fields = ("code", "nom")
    list_editable = ("statut",)
    inlines = [ECInline]


@admin.register(EC)
class ECAdmin(admin.ModelAdmin):
    list_display = ("code", "nom", "ue")
    list_filter = ("ue",)


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ("matricule", "nom", "prenom", "annee_promo")
    search_fields = ("matricule", "nom", "prenom")


@admin.register(NoteEC)
class NoteECAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "ec", "note", "import_fichier")
    list_filter = ("ec__ue",)
    search_fields = ("etudiant__nom", "etudiant__matricule")


@admin.register(ResultatUE)
class ResultatUEAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "ue", "moyenne_ue", "statut", "import_fichier")
    list_filter = ("statut", "ue")
    search_fields = ("etudiant__nom", "etudiant__matricule")
