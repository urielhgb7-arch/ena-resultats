from django.contrib import admin
from .models import AnneeAcademique, Niveau, Filiere, Specialite, Semestre, SessionResultat

@admin.register(AnneeAcademique)
class AnneeAcademiqueAdmin(admin.ModelAdmin):
    list_display = ("libelle", "active")
    list_filter = ("active",)
    search_fields = ("libelle",)


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ("libelle", "annee")
    list_filter = ("annee",)
    search_fields = ("libelle",)


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ("nom", "niveau", "a_des_specialites", "specialite_unique_auto")
    list_filter = ("niveau", "a_des_specialites", "specialite_unique_auto")
    search_fields = ("nom",)


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ("nom", "filiere")
    list_filter = ("filiere",)
    search_fields = ("nom",)


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ("libelle", "filiere", "type")
    list_filter = ("type", "filiere")
    search_fields = ("libelle",)


@admin.register(SessionResultat)
class SessionResultatAdmin(admin.ModelAdmin):
    list_display = ("get_type_display", "semestre", "specialite")
    list_filter = ("type", "semestre")
    search_fields = ("semestre__libelle", "specialite__nom")
