from django import forms
from .models import ImportFichier

class ImportFichierForm(forms.ModelForm):
    class Meta:
        model = ImportFichier
        fields = ["fichier"]
        widgets = {
            "fichier": forms.ClearableFileInput(attrs={
                "class": "hidden",
                "id": "file-upload"
            })
        }
