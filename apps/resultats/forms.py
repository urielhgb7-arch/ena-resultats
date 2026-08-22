from django import forms
from .models import UE, ContactSignalement

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

class ContactSignalementForm(forms.ModelForm):
    class Meta:
        model = ContactSignalement
        fields = ['nom', 'email', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-black/15 rounded-xl focus:border-[#1F6F4A] focus:ring-2 focus:ring-[#1F6F4A]/20 focus:outline-none transition shadow-sm',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-black/15 rounded-xl focus:border-[#1F6F4A] focus:ring-2 focus:ring-[#1F6F4A]/20 focus:outline-none transition shadow-sm',
                'placeholder': 'votre.email@ena.bj'
            }),
            'sujet': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-black/15 rounded-xl focus:border-[#1F6F4A] focus:ring-2 focus:ring-[#1F6F4A]/20 focus:outline-none transition shadow-sm',
                'placeholder': 'Sujet de votre message'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-black/15 rounded-xl focus:border-[#1F6F4A] focus:ring-2 focus:ring-[#1F6F4A]/20 focus:outline-none transition shadow-sm',
                'placeholder': 'Détaillez votre demande ou signalement...',
                'rows': 5
            }),
        }
