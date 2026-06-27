from django.db.models import Count
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Enseignant, Grade, Profil, Specialite
from .form import EnseignantForm, GradeForm, ProfilForm, SpecialiteForm


def home(request):
    enseignants = Enseignant.objects.select_related('specialite', 'profil', 'grade').all()

    return render(
        request,
        'gestion_ensg/home.html',
        {
            'enseignants': enseignants,
            'enseignants_count': enseignants.count(),
            'specialites_count': Specialite.objects.count(),
            'profils_count': Profil.objects.count(),
            'grades_count': Grade.objects.count(),
        }
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
    form = SpecialiteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Specialite ajoutee avec succes.')
        return redirect('gestion_ensg:specialites')

    return render(
        request,
        'gestion_ensg/specialites.html',
        {
            'form': form,
            'specialites': Specialite.objects.annotate(
                enseignants_count=Count('enseignant')
            ).order_by('nom'),
            'specialites_count': Specialite.objects.count(),
        }
    )


def update_specialite(request, pk):
    specialite = get_object_or_404(Specialite, pk=pk)
    form = SpecialiteForm(request.POST or None, instance=specialite)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Specialite modifiee avec succes.')
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
        nom = specialite.nom
        enseignants_count = specialite.enseignant_set.count()
        specialite.delete()
        if enseignants_count:
            messages.warning(
                request,
                f'Specialite "{nom}" supprimee. {enseignants_count} enseignant(s) restent sans specialite.'
            )
        else:
            messages.success(request, f'Specialite "{nom}" supprimee avec succes.')

    return redirect('gestion_ensg:specialites')


def profils(request):
    form = ProfilForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('gestion_ensg:profils')

    return render(
        request,
        'gestion_ensg/profils.html',
        {
            'form': form,
            'profils': Profil.objects.annotate(
                enseignants_count=Count('enseignant')
            ).order_by('nom'),
            'profils_count': Profil.objects.count(),
        }
    )


def update_profil(request, pk):
    profil = get_object_or_404(Profil, pk=pk)
    form = ProfilForm(request.POST or None, instance=profil)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('gestion_ensg:profils')

    return render(
        request,
        'gestion_ensg/update_profil.html',
        {
            'form': form,
            'profil': profil,
        }
    )


def delete_profil(request, pk):
    profil = get_object_or_404(Profil, pk=pk)

    if request.method == 'POST':
        profil.delete()

    return redirect('gestion_ensg:profils')


def grades(request):
    form = GradeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('gestion_ensg:grades')

    return render(
        request,
        'gestion_ensg/grades.html',
        {
            'form': form,
            'grades': Grade.objects.annotate(
                enseignants_count=Count('enseignant')
            ).order_by('nom'),
            'grades_count': Grade.objects.count(),
        }
    )


def update_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    form = GradeForm(request.POST or None, instance=grade)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('gestion_ensg:grades')

    return render(
        request,
        'gestion_ensg/update_grade.html',
        {
            'form': form,
            'grade': grade,
        }
    )


def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)

    if request.method == 'POST':
        grade.delete()

    return redirect('gestion_ensg:grades')


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
