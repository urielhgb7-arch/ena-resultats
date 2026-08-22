from django import forms
from .models import ImportFichier
from apps.filieres.models import AnneeAcademique

class ImportFichierForm(forms.ModelForm):
    # Champ non lié au modèle pour amorcer la cascade
    annee = forms.ModelChoiceField(
        queryset=AnneeAcademique.objects.all(),
        required=False,
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
        fields = ["session", "mapping", "fichier"]
        widgets = {
            "session": forms.Select(attrs={
                "class": "w-full border border-black/15 rounded-xl px-3 py-2 text-sm focus:ring-[#1F6F4A] focus:border-[#1F6F4A]",
                "id": "select-session",
                "x-model": "session",
                "required": "required",
                ":disabled": "!semestre"
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
