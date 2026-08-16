from django.contrib import admin
from .models import MappingTemplate, ImportFichier, LigneBrute


@admin.register(MappingTemplate)
class MappingTemplateAdmin(admin.ModelAdmin):
    list_display = ("nom",)


class LigneBruteInline(admin.TabularInline):
    model = LigneBrute
    extra = 0
    readonly_fields = ("numero_ligne", "donnees_brutes", "statut_traitement")
    can_delete = False


@admin.register(ImportFichier)
class ImportFichierAdmin(admin.ModelAdmin):
    list_display = ("nom_fichier", "date_import", "utilisateur", "statut")
    list_filter = ("statut",)
    inlines = [LigneBruteInline]
