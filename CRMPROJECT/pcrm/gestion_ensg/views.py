from django.shortcuts import get_object_or_404, render, redirect
from .models import Enseignant, Specialite
from .form import EnseignantForm, SpecialiteForm


DEFAULT_SPECIALITES = [
    'Geodesie',
    'Topographie',
    'Geomatique',
    'Cartographie',
    'Photogrammetrie',
    'Teledetection',
    'SIG',
    'Informatique',
]


def create_default_specialites():
    for nom in DEFAULT_SPECIALITES:
        Specialite.objects.get_or_create(nom=nom)


def home(request):

    enseignants = Enseignant.objects.all()

    return render(
        request,
        'gestion_ensg/home.html',
        {'enseignants': enseignants}
    )


def add_record(request):

    form = EnseignantForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('gestion_ensg:home')

    return render(
        request,
        'gestion_ensg/add_record.html',
        {'form': form}
    )


def specialites(request):
    create_default_specialites()

    form = SpecialiteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('gestion_ensg:specialites')

    return render(
        request,
        'gestion_ensg/specialites.html',
        {
            'form': form,
            'specialites': Specialite.objects.all(),
        }
    )


def update_specialite(request, pk):
    specialite = get_object_or_404(Specialite, pk=pk)
    form = SpecialiteForm(request.POST or None, instance=specialite)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('gestion_ensg:specialites')

    return render(
        request,
        'gestion_ensg/update_specialite.html',
        {
            'form': form,
            'specialite': specialite,
        }
    )


def delete_specialite(request, pk):
    specialite = get_object_or_404(Specialite, pk=pk)

    if request.method == 'POST':
        specialite.delete()

    return redirect('gestion_ensg:specialites')


def record(request, pk):

    enseignant = Enseignant.objects.get(id=pk)

    return render(
        request,
        'gestion_ensg/record.html',
        {'enseignant': enseignant}
    )


def update_record(request, pk):

    enseignant = Enseignant.objects.get(id=pk)

    form = EnseignantForm(
        request.POST or None,
        instance=enseignant
    )

    if form.is_valid():
        form.save()
        return redirect('gestion_ensg:home')

    return render(
        request,
        'gestion_ensg/update_record.html',
        {'form': form}
    )


def delete_record(request, pk):

    enseignant = Enseignant.objects.get(id=pk)

    if request.method == 'POST':
        enseignant.delete()
        return redirect('gestion_ensg:home')

    return render(
        request,
        'gestion_ensg/delete.html',
        {'enseignant': enseignant}
    )
