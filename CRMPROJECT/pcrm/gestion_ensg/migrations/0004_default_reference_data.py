from django.db import migrations


DEFAULT_SPECIALITES = [
    'marketing digital et data analytics',
    'marketing digital et logistique international',
    'management international',
    'finance et audit',
    'droit public',
    'SIG',
    'Informatique',
]

DEFAULT_PROFILS = [
    'Permanent',
    'Vacataire',
    'Contractuel',
    'Intervenant externe',
]

DEFAULT_GRADES = [
    'Professeur assistant',
    'Professeur habilite',
    'Professeur de l enseignement superieur',
    'Maitre de conferences',
    'Doctorant',
]


def create_default_reference_data(apps, schema_editor):
    Specialite = apps.get_model('gestion_ensg', 'Specialite')
    Profil = apps.get_model('gestion_ensg', 'Profil')
    Grade = apps.get_model('gestion_ensg', 'Grade')

    for nom in DEFAULT_SPECIALITES:
        Specialite.objects.get_or_create(nom=nom)

    for nom in DEFAULT_PROFILS:
        Profil.objects.get_or_create(nom=nom)

    for nom in DEFAULT_GRADES:
        Grade.objects.get_or_create(nom=nom)


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_ensg', '0003_grade_profil_alter_enseignant_specialite_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_reference_data, migrations.RunPython.noop),
    ]
