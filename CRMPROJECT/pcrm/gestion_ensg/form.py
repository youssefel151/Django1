from django import forms
from .models import Enseignant, Specialite

class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = '__all__'


class SpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialite
        fields = ['nom']
