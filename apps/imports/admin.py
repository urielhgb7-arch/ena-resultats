from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin, messages
from django.utils.html import format_html
from django_q.tasks import async_task

from .models import MappingTemplate, ImportFichier, LigneBrute
from .tasks import process_import_staging_task, process_import_validation_task


@admin.register(MappingTemplate)
class MappingTemplateAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


class LigneBruteInline(admin.TabularInline):
    model = LigneBrute
    extra = 0
    readonly_fields = ("numero_ligne", "donnees_brutes", "statut_traitement", "message_erreur")
    can_delete = False
    max_num = 20  # Affiche les 20 premières lignes pour aperçu rapide
    show_change_link = True


@admin.register(ImportFichier)
class ImportFichierAdmin(SimpleHistoryAdmin):
    list_display = ("nom_fichier", "statut_badge", "date_import", "utilisateur", "mapping", "stats_lignes")
    list_filter = ("statut", "date_import", "mapping")
    search_fields = ("nom_fichier",)
    search_help_text = "Recherche par nom de fichier"
    inlines = [LigneBruteInline]
    actions = ["action_appliquer_import", "action_relancer_staging"]

    @admin.display(description="Statut")
    def statut_badge(self, obj):
        colors = {
            "en_attente": "#f59e0b",  # Orange
            "valide": "#3b82f6",      # Bleu
            "applique": "#10b981",    # Vert
            "annule": "#ef4444",      # Rouge
        }
        color = colors.get(obj.statut, "#6b7280")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.get_statut_display()
        )

    @admin.display(description="Progression / Lignes")
    def stats_lignes(self, obj):
        total = obj.lignes.count()
        if total == 0:
            return "0 ligne"
        traitees = obj.lignes.filter(statut_traitement="traite").count()
        erreurs = obj.lignes.filter(statut_traitement="erreur").count()
        return format_html(
            "<b>{}</b> total (✅ {} traitées, ⚠️ {} erreurs)",
            total,
            traitees,
            erreurs
        )

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        if is_new:
            obj.utilisateur = request.user
            
        super().save_model(request, obj, form, change)
        
        # Déclenchement asynchrone du staging via Django-Q2
        if is_new and obj.fichier:
            async_task(process_import_staging_task, obj.pk)
            messages.info(
                request,
                f"Le fichier '{obj.nom_fichier}' a été téléversé. Le staging asynchrone est en cours d'exécution."
            )

    @admin.action(description="⚡ Appliquer le mapping et insérer les résultats (Asynchrone)")
    def action_appliquer_import(self, request, queryset):
        dispatched = 0
        for import_obj in queryset:
            if not import_obj.mapping:
                messages.warning(
                    request,
                    f"Impossible d'appliquer l'import '{import_obj.nom_fichier}' : aucun template de mapping sélectionné."
                )
                continue

            async_task(process_import_validation_task, import_obj.pk)
            dispatched += 1

        if dispatched > 0:
            messages.success(
                request,
                f"{dispatched} import(s) envoyé(s) au cluster d'arrière-plan pour application et calcul des résultats."
            )

    @admin.action(description="🔄 Relancer le découpage en lignes brutes (Staging)")
    def action_relancer_staging(self, request, queryset):
        for import_obj in queryset:
            async_task(process_import_staging_task, import_obj.pk)
        messages.info(request, f"Staging relancé en arrière-plan pour {queryset.count()} fichier(s).")


@admin.register(LigneBrute)
class LigneBruteAdmin(admin.ModelAdmin):
    list_display = ("numero_ligne", "import_fichier", "statut_badge", "message_erreur_courte", "apercu_donnees")
    list_filter = ("statut_traitement", "import_fichier")
    search_fields = ("numero_ligne", "message_erreur", "donnees_brutes")
    readonly_fields = ("import_fichier", "numero_ligne", "donnees_brutes", "statut_traitement", "message_erreur")

    @admin.display(description="Statut")
    def statut_badge(self, obj):
        colors = {
            "en_attente": "#f59e0b",
            "traite": "#10b981",
            "erreur": "#ef4444",
        }
        color = colors.get(obj.statut_traitement, "#6b7280")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 8px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.statut_traitement
        )

    @admin.display(description="Erreur / Motif")
    def message_erreur_courte(self, obj):
        if not obj.message_erreur:
            return "-"
        return format_html('<span style="color: #ef4444; font-weight: 500;">{}</span>', obj.message_erreur)

    @admin.display(description="Données Brutes (JSON)")
    def apercu_donnees(self, obj):
        raw_str = str(obj.donnees_brutes)
        if len(raw_str) > 80:
            return raw_str[:80] + "..."
        return raw_str
