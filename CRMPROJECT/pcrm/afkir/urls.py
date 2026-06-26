from django.urls import path
from . import views

app_name = 'afkir'

urlpatterns = [
    path('', views.liste_etudiants, name='liste_etudiants'),
    path('ajouter/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('inscrire/', views.inscrire_etudiant, name='inscrire_etudiant'),
    path('modifier/<int:pk>/', views.modifier_etudiant, name='modifier_etudiant'),
    path('supprimer/<int:pk>/', views.supprimer_etudiant, name='supprimer_etudiant'),
]
