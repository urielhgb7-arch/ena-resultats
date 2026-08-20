from django import forms
from .models import Filiere

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ["niveau", "nom", "a_des_specialites", "specialite_unique_auto"]
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "w-full bg-surface border border-bordercol rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-violet focus:ring-1 focus:ring-brand-violet transition-colors",
                "placeholder": "Ex: Mathématiques et Informatique"
            }),
            "niveau": forms.Select(attrs={
                "class": "w-full bg-surface border border-bordercol rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-violet focus:ring-1 focus:ring-brand-violet transition-colors"
            }),
            "a_des_specialites": forms.CheckboxInput(attrs={
                "class": "w-5 h-5 rounded bg-surface border-bordercol text-brand-violet focus:ring-brand-violet focus:ring-offset-surface"
            }),
            "specialite_unique_auto": forms.CheckboxInput(attrs={
                "class": "w-5 h-5 rounded bg-surface border-bordercol text-brand-violet focus:ring-brand-violet focus:ring-offset-surface"
            }),
        }
