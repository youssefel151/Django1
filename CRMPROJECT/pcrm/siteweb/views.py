import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Avg, Count, Max, Min, Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .authz import get_user_role, role_required
from .form import (
    AddRecordForm,
    EtudiantForm,
    NoteForm,
    SignUpForm,
)
from .models import Etudiant, Note, Profile, Record


@never_cache
@ensure_csrf_cookie
def home(request):
    #verification de methode de s'aunthentification
    if request.method=="POST":
       username = request.POST.get('username')
       password = request.POST.get('password')
       #verification des donnes username et mode de passe
       user = authenticate(request,username=username,password=password)
       if user is not None:
            login(request, user)
            messages.success(request, "Bien s'authentifier!! ")
            return redirect("dashboard")
       else:
            messages.error(request,"Erreur authentification...")
            return redirect("home")
    else:
        records = None
        if request.user.is_authenticated and get_user_role(request.user) == Profile.ROLE_ADMIN:
            records = Record.objects.all()
        return render(request, 'home.html', {'records' : records})


def logout_user(request):
    logout(request)
    messages.success(request, "Bien se deconnecter ...")
    return redirect('home')

@never_cache
@ensure_csrf_cookie
def register_user(request):
    if request.method=="POST":
        f=SignUpForm(request.POST)
        if f.is_valid():
            user = f.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'role': f.cleaned_data['role'],
                    'phone': f.cleaned_data['phone'],
                    'department': f.cleaned_data['department'],
                    'student_number': f.cleaned_data['student_number'],
                },
            )

            username=f.cleaned_data['username']
            password=f.cleaned_data['password1']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

            messages.success(request, "Bien inscrit!!!")
            return redirect('dashboard')
        return render(request, 'register.html', {'form':f})
    f=SignUpForm()
    return render(request, 'register.html', {'form':f})


@login_required
def dashboard(request):
    role = get_user_role(request.user)
    if role == Profile.ROLE_ADMIN:
        return redirect('admin_dashboard')
    if role == Profile.ROLE_ENSEIGNANT:
        return redirect('enseignant_dashboard')
    return redirect('etudiant_dashboard')


@role_required(Profile.ROLE_ADMIN)
def admin_dashboard(request):
    data_filiere = Etudiant.objects.values('filiere').annotate(total=Count('id'))
    context = {
        'teachers_count': Profile.objects.filter(role=Profile.ROLE_ENSEIGNANT).count(),
        'students_count': Profile.objects.filter(role=Profile.ROLE_ETUDIANT).count(),
        'users_count': Profile.objects.count(),
        'records_count': Record.objects.count(),
        'total_etudiants': Etudiant.objects.count(),
        'total_notes': Note.objects.count(),
        'labels': [item['filiere'] for item in data_filiere],
        'counts': [item['total'] for item in data_filiere],
    }
    return render(request, 'dashboard_admin.html', context)


@role_required(Profile.ROLE_ENSEIGNANT)
def enseignant_dashboard(request):
    return render(request, 'dashboard_enseignant.html')


@role_required(Profile.ROLE_ETUDIANT)
def etudiant_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    etudiant = Etudiant.objects.filter(email__iexact=request.user.email).first()
    notes = Note.objects.none()
    stats = {'moyenne': None, 'best_note': None, 'worst_note': None}

    if etudiant:
        notes = Note.objects.filter(etudiant=etudiant)
        stats = notes.aggregate(
            moyenne=Avg('valeur'),
            best_note=Max('valeur'),
            worst_note=Min('valeur'),
        )

    context = {
        'etudiant': etudiant,
        'notes': notes,
        'notes_count': notes.count(),
        'profile': profile,
        'moyenne': round(stats['moyenne'], 2) if stats['moyenne'] is not None else None,
        'best_note': stats['best_note'],
        'worst_note': stats['worst_note'],
    }
    return render(request, 'dashboard_etudiant.html', context)


@role_required(Profile.ROLE_ADMIN)
def customer_record(request, pk):
    if request.user.is_authenticated:
        #voir le record
        cs = get_object_or_404(Record, id=pk)
        return render(request, 'record.html',{'customer_record':cs}) 
    else:
        messages.success(request, "Vous devez etres connecte pour acceder a cette page")
        return redirect('home')

@role_required(Profile.ROLE_ADMIN)
def delete_record(request, pk):
    if request.user.is_authenticated:
        if request.method != "POST":
            messages.error(request, "Veuillez confirmer la suppression depuis le formulaire.")
            return redirect('record', pk=pk)
        delete_it = get_object_or_404(Record, id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully...")
        return redirect('home')
    else:
        messages.success(request, "Vous devez etre connecte")
        return redirect('home')


@role_required(Profile.ROLE_ADMIN)
def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record added successfully...")
                return redirect("home")
        return render(request, "add_record.html", {"form": form})

    messages.success(request, "Vous devez etre connecte pour ajouter un record")
    return redirect("home")



@role_required(Profile.ROLE_ADMIN)
def update_record(request,pk):
    if request.user.is_authenticated:
        current=get_object_or_404(Record, id=pk)
        form=AddRecordForm(request.POST or None,instance=current)
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Record is Updated successfully...")
            return redirect("home")
        return render(request, "update_record.html", {"form": form})
    else:
        messages.success(request, "Vous devez etre connecte pour ajouter un record")
        return redirect("home")


def csrf_failure(request, reason=''):
    messages.error(
        request,
        "La session a expire ou le formulaire est ancien. Veuillez reessayer.",
    )
    return redirect('home')


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def etudiant_list(request):
    query = request.GET.get('q', '')
    filiere_filtre = request.GET.get('filiere', '')
    etudiants = Etudiant.objects.all()
    filiere_list = [f[0] for f in Etudiant.FILIERE_CHOICES]

    if query:
        etudiants = etudiants.filter(
            Q(nom__icontains=query)
            | Q(prenom__icontains=query)
            | Q(filiere__icontains=query)
        )

    if filiere_filtre:
        etudiants = etudiants.filter(filiere=filiere_filtre)

    context = {
        'etudiants': etudiants,
        'query': query,
        'filiere_filtre': filiere_filtre,
        'filiere_list': filiere_list,
    }
    return render(request, 'etudiant_list.html', context)


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def ajouter_etudiant(request):
    form = EtudiantForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Etudiant ajoute avec succes.")
        return redirect('etudiant_list')
    return render(request, 'add_etudiant.html', {'form': form})


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def ajouter_note(request):
    form = NoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        note_instance = form.save(commit=False)
        doublon = Note.objects.filter(
            etudiant=note_instance.etudiant,
            matiere=note_instance.matiere,
        ).exists()

        if doublon:
            form.add_error(
                'matiere',
                "Une note est deja enregistree pour cet etudiant dans cette matiere.",
            )
        else:
            note_instance.save()
            messages.success(request, "Note ajoutee avec succes.")
            return redirect('etudiant_profil', pk=note_instance.etudiant.pk)
    return render(request, 'add_note.html', {'form': form})


@login_required
def etudiant_profil(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if get_user_role(request.user) == Profile.ROLE_ETUDIANT and etudiant.email.lower() != request.user.email.lower():
        messages.error(request, "Vous pouvez consulter uniquement votre propre profil.")
        return redirect('dashboard')

    notes = Note.objects.filter(etudiant=etudiant)
    moyenne = notes.aggregate(Avg('valeur'))['valeur__avg']

    context = {
        'etudiant': etudiant,
        'notes': notes,
        'moyenne': round(moyenne, 2) if moyenne is not None else None,
    }
    return render(request, 'etudiant_profil.html', context)


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def export_etudiants_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Etudiants"
    ws.append(['Nom', 'Prenom', 'Filiere', 'Email'])

    for etudiant in Etudiant.objects.all():
        ws.append([etudiant.nom, etudiant.prenom, etudiant.filiere, etudiant.email])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="liste_etudiants.xlsx"'
    wb.save(response)
    return response


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def modifier_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, instance=note)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Note modifiee avec succes.")
        return redirect('etudiant_profil', pk=note.etudiant.pk)
    return render(request, 'add_note.html', {'form': form})


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def supprimer_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    etudiant_pk = note.etudiant.pk
    note.delete()
    messages.success(request, "Note supprimee avec succes.")
    return redirect('etudiant_profil', pk=etudiant_pk)


@login_required
def generer_bulletin_pdf(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if get_user_role(request.user) == Profile.ROLE_ETUDIANT and etudiant.email.lower() != request.user.email.lower():
        messages.error(request, "Vous pouvez telecharger uniquement votre propre bulletin.")
        return redirect('dashboard')

    notes = Note.objects.filter(etudiant=etudiant)
    moyenne = notes.aggregate(Avg('valeur'))['valeur__avg'] or 0

    context = {'etudiant': etudiant, 'notes': notes, 'moyenne': round(moyenne, 2)}
    html = render_to_string('bulletin_pdf.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bulletin_{etudiant.nom}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur de generation PDF')
    return response


