from django.contrib import admin
from .models import Etudiant, Groupe, Niveau, Note, Parcours, Profile, Record

# Register your models here.
admin.site.register(Record)
admin.site.register(Profile)
admin.site.register(Etudiant)
admin.site.register(Note)


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


@admin.register(Parcours)
class ParcoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'niveau')
    list_filter = ('niveau',)
    search_fields = ('nom', 'code')


@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'parcours', 'capacite')
    list_filter = ('niveau', 'parcours')
    search_fields = ('nom',)
