from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('login', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/enseignant/', views.enseignant_dashboard, name='enseignant_dashboard'),
    path('dashboard/etudiant/', views.etudiant_dashboard, name='etudiant_dashboard'),
    path('etudiants/', views.etudiant_list, name='etudiant_list'),
    path('etudiants/<int:pk>/', views.etudiant_profil, name='etudiant_profil'),
    path('etudiants/ajouter/', views.ajouter_etudiant, name='add_etudiant'),
    path('etudiants/export/', views.export_etudiants_excel, name='export_etudiants_excel'),
    path('notes/ajouter/', views.ajouter_note, name='add_note'),
    path('notes/modifier/<int:pk>/', views.modifier_note, name='modifier_note'),
    path('notes/supprimer/<int:pk>/', views.supprimer_note, name='supprimer_note'),
    path('etudiant/<int:pk>/pdf/', views.generer_bulletin_pdf, name='generer_bulletin_pdf'),
    path('record/<int:pk>/', views.customer_record, name='record'),
    path('delete_record/<int:pk>/', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>/', views.update_record, name='update_record'),
]
