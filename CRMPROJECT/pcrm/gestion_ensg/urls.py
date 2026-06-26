from django.urls import path
from . import views

app_name = 'gestion_ensg'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_record, name='add'),
    path('specialites/', views.specialites, name='specialites'),
    path('specialites/<int:pk>/modifier/', views.update_specialite, name='update_specialite'),
    path('specialites/<int:pk>/supprimer/', views.delete_specialite, name='delete_specialite'),
    path('record/<int:pk>/', views.record, name='record'),
    path('update/<int:pk>/', views.update_record, name='update'),
    path('delete/<int:pk>/', views.delete_record, name='delete'),
]
