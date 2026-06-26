from django import forms
from .models import Etudiant, Inscription


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['code_massar', 'nom', 'prenom', 'email', 'telephone', 'date_naissance']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }


class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['etudiant', 'filiere', 'niveau', 'statut']