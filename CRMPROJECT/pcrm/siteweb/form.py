from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Etudiant, Note, Profile, Record

class SignUpForm(UserCreationForm):
    email=forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    first_name=forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name=forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    role = forms.ChoiceField(
        choices=[
            (Profile.ROLE_ETUDIANT, 'Etudiant'),
            (Profile.ROLE_ENSEIGNANT, 'Enseignant'),
        ],
        label='',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    phone = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}),
    )
    department = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departement / Filiere'}),
    )
    student_number = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero etudiant'}),
    )

    class Meta:
        model=User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'phone',
            'department',
            'student_number',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='User Name'
        self.fields['username'].label=''
        self.fields['username'].help_text='<span class="form-text text-muted"><small>Required, 150 character or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['role'].help_text='<span class="form-text text-muted"><small>Les comptes administrateurs sont crees depuis Django Admin.</small></span>'

        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['placeholder']='Password'
        self.fields['password1'].label=''
        self.fields['password1'].help_text='<span class="form-text text-muted"><small>Your password cannot be too similar to your other personal information.</small></span>'

        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['placeholder']='Confirm Password'
        self.fields['password2'].label=''
        self.fields['password2'].help_text='<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), label='')
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), label='')
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label='')
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), label='')
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}), label='')
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), label='')
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), label='')
    zipcode = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}), label='')

    class Meta:
        model = Record
        # exclude("user",)
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode')


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'email', 'filiere']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['etudiant', 'matiere', 'valeur']
        widgets = {
            'etudiant': forms.Select(attrs={'class': 'form-control'}),
            'matiere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la matiere...'}),
            'valeur': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
