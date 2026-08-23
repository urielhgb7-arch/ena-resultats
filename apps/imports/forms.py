from django import forms
from .models import ImportFichier
from apps.filieres.models import AnneeAcademique

class ImportFichierForm(forms.ModelForm):
    # Champ non lié au modèle pour amorcer la cascade si spécifique,
    # mais maintenant lié à annee_academique pour l'import global
    annee_academique = forms.ModelChoiceField(
        queryset=AnneeAcademique.objects.all(),
        required=True,
        empty_label="— Sélectionner l'année —",
        widget=forms.Select(attrs={
            "class": "w-full border border-black/15 rounded-xl px-3 py-2 text-sm focus:ring-[#1F6F4A] focus:border-[#1F6F4A]",
            "x-model": "annee",
            "hx-get": "/filieres/ajax/niveaux/",
            "hx-target": "#select-niveau",
            "hx-trigger": "change"
        })
    )

    class Meta:
        model = ImportFichier
        fields = ["type_import", "annee_academique", "semestre", "session", "mapping", "fichier"]
        widgets = {
            "type_import": forms.Select(attrs={
                "class": "w-full border border-black/15 rounded-xl px-3 py-2 text-sm focus:ring-[#1F6F4A] focus:border-[#1F6F4A]",
                "x-model": "type_import"
            }),
            "semestre": forms.Select(attrs={
                "class": "w-full border border-black/15 rounded-xl px-3 py-2 text-sm focus:ring-[#1F6F4A] focus:border-[#1F6F4A]",
                "x-model": "semestre_global",
                ":required": "type_import === 'global'",
                ":disabled": "type_import === 'specifique'",
                "x-bind:class": "type_import === 'specifique' ? 'opacity-50 cursor-not-allowed' : ''"
            }),
            "session": forms.Select(attrs={
                "class": "w-full border border-black/15 rounded-xl px-3 py-2 text-sm focus:ring-[#1F6F4A] focus:border-[#1F6F4A]",
                "id": "select-session",
                "x-model": "session",
                ":required": "type_import === 'specifique'",
                ":disabled": "type_import === 'global' || !semestre",
                "x-bind:class": "type_import === 'global' ? 'opacity-50 cursor-not-allowed' : ''"
            }),
            "mapping": forms.Select(attrs={
                "class": "w-full border border-black/15 rounded-xl px-3 py-2 text-sm focus:ring-[#1F6F4A] focus:border-[#1F6F4A]",
                "required": "required"
            }),
            "fichier": forms.ClearableFileInput(attrs={
                "class": "hidden",
                "id": "file-upload",
                "required": "required"
            })
        }
