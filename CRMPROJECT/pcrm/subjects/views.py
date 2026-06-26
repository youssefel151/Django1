from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import AffectationForm, MatiereForm, ProfesseurForm
from .models import Affectation, Matiere, Professeur
from siteweb.authz import RoleRequiredMixin
from siteweb.models import Profile


class StudentSubjectMixin(RoleRequiredMixin):
    allowed_roles = (
        Profile.ROLE_ADMIN,
        Profile.ROLE_ENSEIGNANT,
        Profile.ROLE_ETUDIANT,
    )


class TeacherSubjectMixin(RoleRequiredMixin):
    allowed_roles = (
        Profile.ROLE_ADMIN,
        Profile.ROLE_ENSEIGNANT,
    )


class AdminSubjectMixin(RoleRequiredMixin):
    allowed_roles = (Profile.ROLE_ADMIN,)


class DashboardView(StudentSubjectMixin, TemplateView):
    """Vue du tableau de bord avec statistiques."""

    template_name = 'subjects/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_professeurs'] = Professeur.objects.count()
        context['total_matieres'] = Matiere.objects.count()
        context['total_affectations'] = Affectation.objects.count()
        context['professeurs_actifs'] = Professeur.objects.filter(actif=True).count()
        context['affectations_actives'] = Affectation.objects.filter(actif=True).count()
        context['recent_affectations'] = (
            Affectation.objects.select_related('professeur', 'matiere')
            .order_by('-created_at')[:5]
        )
        return context


class ProfesseurListView(TeacherSubjectMixin, ListView):
    """Liste des professeurs avec recherche et pagination."""

    model = Professeur
    template_name = 'subjects/professeur_list.html'
    context_object_name = 'professeurs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q', '').strip()
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search)
                | Q(prenom__icontains=search)
                | Q(matricule__icontains=search)
                | Q(email__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProfesseurCreateView(AdminSubjectMixin, SuccessMessageMixin, CreateView):
    model = Professeur
    form_class = ProfesseurForm
    template_name = 'subjects/professeur_form.html'
    success_url = reverse_lazy('subjects:professeur_list')
    success_message = 'Professeur ajouté avec succès.'


class ProfesseurDetailView(TeacherSubjectMixin, DetailView):
    model = Professeur
    template_name = 'subjects/professeur_detail.html'
    context_object_name = 'professeur'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['affectations'] = (
            self.object.affectations.select_related('matiere')
            .order_by('-annee_scolaire', 'semestre')
        )
        return context


class ProfesseurUpdateView(AdminSubjectMixin, SuccessMessageMixin, UpdateView):
    model = Professeur
    form_class = ProfesseurForm
    template_name = 'subjects/professeur_form.html'
    success_url = reverse_lazy('subjects:professeur_list')
    success_message = 'Professeur modifié avec succès.'


class ProfesseurDeleteView(AdminSubjectMixin, SuccessMessageMixin, DeleteView):
    model = Professeur
    template_name = 'subjects/professeur_confirm_delete.html'
    success_url = reverse_lazy('subjects:professeur_list')
    success_message = 'Professeur supprimé avec succès.'


class MatiereListView(StudentSubjectMixin, ListView):
    """Liste des matières avec recherche et pagination."""

    model = Matiere
    template_name = 'subjects/matiere_list.html'
    context_object_name = 'matieres'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q', '').strip()
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search)
                | Q(code_matiere__icontains=search)
                | Q(description__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class MatiereCreateView(AdminSubjectMixin, SuccessMessageMixin, CreateView):
    model = Matiere
    form_class = MatiereForm
    template_name = 'subjects/matiere_form.html'
    success_url = reverse_lazy('subjects:matiere_list')
    success_message = 'Matière ajoutée avec succès.'


class MatiereDetailView(StudentSubjectMixin, DetailView):
    model = Matiere
    template_name = 'subjects/matiere_detail.html'
    context_object_name = 'matiere'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['affectations'] = (
            self.object.affectations.select_related('professeur')
            .order_by('-annee_scolaire', 'semestre')
        )
        return context


class MatiereUpdateView(AdminSubjectMixin, SuccessMessageMixin, UpdateView):
    model = Matiere
    form_class = MatiereForm
    template_name = 'subjects/matiere_form.html'
    success_url = reverse_lazy('subjects:matiere_list')
    success_message = 'Matière modifiée avec succès.'


class MatiereDeleteView(AdminSubjectMixin, SuccessMessageMixin, DeleteView):
    model = Matiere
    template_name = 'subjects/matiere_confirm_delete.html'
    success_url = reverse_lazy('subjects:matiere_list')
    success_message = 'Matière supprimée avec succès.'


class AffectationListView(TeacherSubjectMixin, ListView):
    """Liste des affectations avec recherche et pagination."""

    model = Affectation
    template_name = 'subjects/affectation_list.html'
    context_object_name = 'affectations'
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            super().get_queryset()
            .select_related('professeur', 'matiere')
        )
        search = self.request.GET.get('q', '').strip()
        if search:
            queryset = queryset.filter(
                Q(professeur__nom__icontains=search)
                | Q(professeur__prenom__icontains=search)
                | Q(matiere__nom__icontains=search)
                | Q(matiere__code_matiere__icontains=search)
                | Q(annee_scolaire__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class AffectationCreateView(AdminSubjectMixin, SuccessMessageMixin, CreateView):
    model = Affectation
    form_class = AffectationForm
    template_name = 'subjects/affectation_form.html'
    success_url = reverse_lazy('subjects:affectation_list')
    success_message = 'Affectation ajoutée avec succès.'

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erreur lors de la création. Veuillez corriger les champs indiqués.',
        )
        return super().form_invalid(form)


class AffectationUpdateView(AdminSubjectMixin, SuccessMessageMixin, UpdateView):
    model = Affectation
    form_class = AffectationForm
    template_name = 'subjects/affectation_form.html'
    success_url = reverse_lazy('subjects:affectation_list')
    success_message = 'Affectation modifiée avec succès.'

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erreur lors de la modification. Veuillez corriger les champs indiqués.',
        )
        return super().form_invalid(form)


class AffectationDeleteView(AdminSubjectMixin, SuccessMessageMixin, DeleteView):
    model = Affectation
    template_name = 'subjects/affectation_confirm_delete.html'
    success_url = reverse_lazy('subjects:affectation_list')
    success_message = 'Affectation supprimée avec succès.'
