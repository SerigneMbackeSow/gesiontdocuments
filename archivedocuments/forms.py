from django import forms
from .models import Dossiers

class DossiersForm(forms.ModelForm):
    class Meta:
        model = Dossiers
        fields = ['date_creation', 'nom', 'direction', 'id_parent']
