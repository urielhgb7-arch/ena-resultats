from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from .models import MappingTemplate, ImportFichier, LigneBrute

@admin.register(MappingTemplate)
class MappingTemplateAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


import openpyxl
from django.contrib import messages
from django.db import transaction

@admin.register(ImportFichier)
class ImportFichierAdmin(SimpleHistoryAdmin):
    list_display = ("nom_fichier", "date_import", "utilisateur", "statut")
    list_filter = ("statut", "date_import")
    search_fields = ("nom_fichier",)
    search_help_text = "Recherche par nom de fichier"

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        if is_new:
            obj.utilisateur = request.user
            
        super().save_model(request, obj, form, change)
        
        if is_new and obj.fichier:
            try:
                wb = openpyxl.load_workbook(obj.fichier.path, data_only=True)
                sheet = wb.active
                
                rows = list(sheet.iter_rows(values_only=True))
                if len(rows) > 1:
                    headers = [str(h).strip() if h else f"col_{i}" for i, h in enumerate(rows[0])]
                    lignes_brutes = []
                    
                    for i, row in enumerate(rows[1:], start=2):
                        donnees = {}
                        has_data = False
                        for j, val in enumerate(row):
                            # Ensure JSON serializable string/number/null
                            if val is not None:
                                has_data = True
                                donnees[headers[j]] = str(val) if not isinstance(val, (int, float, bool)) else val
                            else:
                                donnees[headers[j]] = None
                                
                        if has_data:
                            lignes_brutes.append(LigneBrute(
                                import_fichier=obj,
                                numero_ligne=i,
                                donnees_brutes=donnees
                            ))
                            
                    if lignes_brutes:
                        with transaction.atomic():
                            LigneBrute.objects.bulk_create(lignes_brutes)
                            
            except Exception as e:
                messages.error(request, f"Erreur lors du traitement du fichier Excel : {str(e)}")


@admin.register(LigneBrute)
class LigneBruteAdmin(admin.ModelAdmin):
    list_display = ("numero_ligne", "import_fichier", "statut_traitement")
    list_filter = ("statut_traitement", "import_fichier")
    search_fields = ("numero_ligne",)
