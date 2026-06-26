from django.contrib import admin

from .models import Affectation, Matiere, Professeur


@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = (
        'matricule', 'nom', 'prenom', 'email', 'specialite',
        'date_embauche', 'actif', 'created_at',
    )
    list_filter = ('actif', 'specialite', 'date_embauche')
    search_fields = ('matricule', 'nom', 'prenom', 'email', 'specialite')
    ordering = ('nom', 'prenom')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('matricule', 'nom', 'prenom', 'email', 'telephone'),
        }),
        ('Informations professionnelles', {
            'fields': ('specialite', 'date_embauche', 'actif'),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = (
        'code_matiere', 'nom', 'niveau', 'coefficient',
        'volume_horaire', 'created_at',
    )
    list_filter = ('niveau', 'coefficient')
    search_fields = ('code_matiere', 'nom', 'description')
    ordering = ('niveau', 'nom')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations générales', {
            'fields': ('code_matiere', 'nom', 'description', 'niveau'),
        }),
        ('Paramètres pédagogiques', {
            'fields': ('coefficient', 'volume_horaire'),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = (
        'professeur', 'matiere', 'annee_scolaire', 'semestre',
        'date_affectation', 'actif',
    )
    list_filter = ('annee_scolaire', 'semestre', 'actif', 'matiere__niveau')
    search_fields = (
        'professeur__nom', 'professeur__prenom', 'professeur__matricule',
        'matiere__nom', 'matiere__code_matiere', 'annee_scolaire',
    )
    ordering = ('-annee_scolaire', 'semestre')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('professeur', 'matiere')
    fieldsets = (
        ('Affectation', {
            'fields': ('professeur', 'matiere', 'annee_scolaire', 'semestre'),
        }),
        ('Détails', {
            'fields': ('date_affectation', 'commentaire', 'actif'),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
