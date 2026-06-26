from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard_alt'),

    # Professeurs
    path('professeurs/', views.ProfesseurListView.as_view(), name='professeur_list'),
    path('professeurs/create/', views.ProfesseurCreateView.as_view(), name='professeur_create'),
    path('professeurs/<int:pk>/', views.ProfesseurDetailView.as_view(), name='professeur_detail'),
    path(
        'professeurs/<int:pk>/update/',
        views.ProfesseurUpdateView.as_view(),
        name='professeur_update',
    ),
    path(
        'professeurs/<int:pk>/delete/',
        views.ProfesseurDeleteView.as_view(),
        name='professeur_delete',
    ),

    # Matières
    path('matieres/', views.MatiereListView.as_view(), name='matiere_list'),
    path('matieres/create/', views.MatiereCreateView.as_view(), name='matiere_create'),
    path('matieres/<int:pk>/', views.MatiereDetailView.as_view(), name='matiere_detail'),
    path(
        'matieres/<int:pk>/update/',
        views.MatiereUpdateView.as_view(),
        name='matiere_update',
    ),
    path(
        'matieres/<int:pk>/delete/',
        views.MatiereDeleteView.as_view(),
        name='matiere_delete',
    ),

    # Affectations
    path('affectations/', views.AffectationListView.as_view(), name='affectation_list'),
    path(
        'affectations/create/',
        views.AffectationCreateView.as_view(),
        name='affectation_create',
    ),
    path(
        'affectations/<int:pk>/update/',
        views.AffectationUpdateView.as_view(),
        name='affectation_update',
    ),
    path(
        'affectations/<int:pk>/delete/',
        views.AffectationDeleteView.as_view(),
        name='affectation_delete',
    ),
]
