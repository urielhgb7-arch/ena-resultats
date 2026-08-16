from django.contrib import admin
from .models import AnneeAcademique, Niveau, Filiere, Specialite, Semestre, SessionResultat


@admin.register(AnneeAcademique)
class AnneeAcademiqueAdmin(admin.ModelAdmin):
    list_display = ("libelle", "active")
    list_editable = ("active",)


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ("libelle", "annee")
    list_filter = ("annee",)


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ("nom", "niveau", "a_des_specialites", "specialite_unique_auto")
    list_filter = ("niveau", "a_des_specialites", "specialite_unique_auto")
    list_editable = ("a_des_specialites", "specialite_unique_auto")
    search_fields = ("nom",)


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ("nom", "filiere")
    list_filter = ("filiere",)


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ("libelle", "filiere", "type")
    list_filter = ("filiere", "type")


@admin.register(SessionResultat)
class SessionResultatAdmin(admin.ModelAdmin):
    list_display = ("type", "semestre", "specialite")
    list_filter = ("type", "semestre__filiere")
