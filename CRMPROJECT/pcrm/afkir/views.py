from django.shortcuts import get_object_or_404, render, redirect
from siteweb.authz import role_required
from siteweb.models import Profile
from .models import Etudiant, Inscription
from .forms import EtudiantForm, InscriptionForm


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def liste_etudiants(request):
    etudiants = Etudiant.objects.all()
    inscriptions = Inscription.objects.all()
    return render(request, 'etudiants/liste.html', {
        'etudiants': etudiants,
        'inscriptions': inscriptions
    })


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def ajouter_etudiant(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('afkir:liste_etudiants')
    else:
        form = EtudiantForm()
    return render(request, 'etudiants/ajouter_etudiant.html', {'form': form})


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def inscrire_etudiant(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('afkir:liste_etudiants')
    else:
        form = InscriptionForm()
    return render(request, 'etudiants/inscrire_etudiant.html', {'form': form})


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def modifier_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            return redirect('afkir:liste_etudiants')
    else:
        form = EtudiantForm(instance=etudiant)
    return render(request, 'etudiants/ajouter_etudiant.html', {'form': form, 'modifier': True})


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def supprimer_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        etudiant.delete()
        return redirect('afkir:liste_etudiants')
    return render(request, 'etudiants/supprimer_confirmation.html', {'etudiant': etudiant})
