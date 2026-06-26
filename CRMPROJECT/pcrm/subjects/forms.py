from django import forms
from django.core.exceptions import ValidationError

from .models import Affectation, Matiere, Professeur


class BootstrapModelForm(forms.ModelForm):
    """Formulaire de base avec classes Bootstrap 5."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class


class ProfesseurForm(BootstrapModelForm):
    class Meta:
        model = Professeur
        fields = [
            'matricule', 'nom', 'prenom', 'email', 'telephone',
            'specialite', 'date_embauche', 'actif',
        ]
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
        }


class MatiereForm(BootstrapModelForm):
    class Meta:
        model = Matiere
        fields = [
            'code_matiere', 'nom', 'description', 'coefficient',
            'volume_horaire', 'niveau',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AffectationForm(BootstrapModelForm):
    class Meta:
        model = Affectation
        fields = [
            'professeur', 'matiere', 'annee_scolaire', 'semestre',
            'date_affectation', 'commentaire', 'actif',
        ]
        widgets = {
            'date_affectation': forms.DateInput(attrs={'type': 'date'}),
            'commentaire': forms.Textarea(attrs={'rows': 3}),
            'professeur': forms.Select(attrs={'class': 'form-select'}),
            'matiere': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['professeur'].queryset = Professeur.objects.filter(actif=True)
        self.fields['matiere'].queryset = Matiere.objects.all().order_by('nom')

    def clean(self):
        cleaned_data = super().clean()
        professeur = cleaned_data.get('professeur')
        matiere = cleaned_data.get('matiere')
        annee_scolaire = cleaned_data.get('annee_scolaire')
        semestre = cleaned_data.get('semestre')

        if not all([professeur, matiere, annee_scolaire, semestre]):
            return cleaned_data

        queryset = Affectation.objects.filter(
            professeur=professeur,
            matiere=matiere,
            annee_scolaire=annee_scolaire,
            semestre=semestre,
        )
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(
                'Une affectation existe déjà pour ce professeur, '
                'cette matière, cette année scolaire et ce semestre.'
            )

        return cleaned_data
