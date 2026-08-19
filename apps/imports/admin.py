from django.contrib import admin
from .models import MappingTemplate, ImportFichier, LigneBrute

@admin.register(MappingTemplate)
class MappingTemplateAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


@admin.register(ImportFichier)
class ImportFichierAdmin(admin.ModelAdmin):
    list_display = ("nom_fichier", "date_import", "utilisateur", "statut")
    list_filter = ("statut", "date_import")
    search_fields = ("nom_fichier",)
    search_help_text = "Recherche par nom de fichier"


@admin.register(LigneBrute)
class LigneBruteAdmin(admin.ModelAdmin):
    list_display = ("numero_ligne", "import_fichier", "statut_traitement")
    list_filter = ("statut_traitement", "import_fichier")
    search_fields = ("numero_ligne",)
