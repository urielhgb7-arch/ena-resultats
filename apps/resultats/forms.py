from django import forms
from .models import UE

class UEForm(forms.ModelForm):
    class Meta:
        model = UE
        fields = ["session", "code", "nom", "credits", "date_publication", "statut"]
        widgets = {
            "code": forms.TextInput(attrs={
                "class": "w-full bg-surface border border-bordercol rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-violet focus:ring-1 focus:ring-brand-violet transition-colors",
                "placeholder": "Ex: MTH1121"
            }),
            "nom": forms.TextInput(attrs={
                "class": "w-full bg-surface border border-bordercol rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-violet focus:ring-1 focus:ring-brand-violet transition-colors",
                "placeholder": "Ex: Mathématiques Générales"
            }),
            "session": forms.Select(attrs={
                "class": "w-full bg-surface border border-bordercol rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-violet focus:ring-1 focus:ring-brand-violet transition-colors"
            }),
            "credits": forms.NumberInput(attrs={
                "class": "w-full bg-surface border border-bordercol rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-violet focus:ring-1 focus:ring-brand-violet transition-colors",
                "min": "1"
            }),
            "date_publication": forms.DateInput(format='%Y-%m-%d', attrs={
                "class": "w-full bg-surface border border-bordercol rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-violet focus:ring-1 focus:ring-brand-violet transition-colors",
                "type": "date"
            }),
            "statut": forms.Select(attrs={
                "class": "w-full bg-surface border border-bordercol rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-violet focus:ring-1 focus:ring-brand-violet transition-colors"
            }),
        }
