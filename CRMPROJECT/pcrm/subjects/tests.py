from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from .models import Affectation, Matiere, Professeur


class ProfesseurModelTest(TestCase):
    """Tests unitaires pour le modèle Professeur."""

    def setUp(self):
        self.professeur = Professeur.objects.create(
            matricule='PROF001',
            nom='Dupont',
            prenom='Jean',
            email='jean.dupont@school.fr',
            telephone='0601020304',
            specialite='Mathématiques',
            date_embauche=date(2020, 9, 1),
            actif=True,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.professeur), 'Jean Dupont (PROF001)')

    def test_nom_complet_property(self):
        self.assertEqual(self.professeur.nom_complet, 'Jean Dupont')

    def test_matricule_unique(self):
        with self.assertRaises(IntegrityError):
            Professeur.objects.create(
                matricule='PROF001',
                nom='Martin',
                prenom='Paul',
                email='paul.martin@school.fr',
                telephone='0605060708',
                specialite='Physique',
                date_embauche=date(2021, 9, 1),
            )


class MatiereModelTest(TestCase):
    """Tests unitaires pour le modèle Matiere."""

    def setUp(self):
        self.matiere = Matiere.objects.create(
            code_matiere='MAT101',
            nom='Algèbre',
            description='Introduction à l\'algèbre',
            coefficient=3.0,
            volume_horaire=60,
            niveau='1ere',
        )

    def test_str_representation(self):
        self.assertEqual(str(self.matiere), 'MAT101 - Algèbre')

    def test_code_matiere_unique(self):
        with self.assertRaises(IntegrityError):
            Matiere.objects.create(
                code_matiere='MAT101',
                nom='Géométrie',
                coefficient=2.0,
                volume_horaire=45,
                niveau='2eme',
            )


class AffectationModelTest(TestCase):
    """Tests unitaires pour le modèle Affectation."""

    def setUp(self):
        self.professeur = Professeur.objects.create(
            matricule='PROF002',
            nom='Bernard',
            prenom='Marie',
            email='marie.bernard@school.fr',
            telephone='0611223344',
            specialite='Informatique',
            date_embauche=date(2019, 9, 1),
        )
        self.matiere = Matiere.objects.create(
            code_matiere='INF201',
            nom='Programmation Python',
            coefficient=4.0,
            volume_horaire=80,
            niveau='2eme',
        )
        self.affectation = Affectation.objects.create(
            professeur=self.professeur,
            matiere=self.matiere,
            annee_scolaire='2024-2025',
            semestre=1,
            date_affectation=date(2024, 9, 15),
        )

    def test_str_representation(self):
        expected = 'Marie Bernard - Programmation Python (2024-2025, S1)'
        self.assertEqual(str(self.affectation), expected)

    def test_unique_constraint(self):
        with self.assertRaises(ValidationError):
            Affectation.objects.create(
                professeur=self.professeur,
                matiere=self.matiere,
                annee_scolaire='2024-2025',
                semestre=1,
                date_affectation=date(2024, 10, 1),
            )

    def test_invalid_annee_scolaire_format(self):
        affectation = Affectation(
            professeur=self.professeur,
            matiere=self.matiere,
            annee_scolaire='2024',
            semestre=2,
            date_affectation=date(2024, 9, 15),
        )
        with self.assertRaises(ValidationError):
            affectation.full_clean()

    def test_inactive_professeur_validation(self):
        self.professeur.actif = False
        self.professeur.save()
        affectation = Affectation(
            professeur=self.professeur,
            matiere=self.matiere,
            annee_scolaire='2025-2026',
            semestre=2,
            date_affectation=date(2025, 9, 15),
        )
        with self.assertRaises(ValidationError):
            affectation.full_clean()


class DashboardViewTest(TestCase):
    """Tests pour la vue Dashboard."""

    def setUp(self):
        self.client = Client()

    def test_dashboard_status_code(self):
        response = self.client.get(reverse('subjects:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tableau de bord')

    def test_dashboard_statistics(self):
        Professeur.objects.create(
            matricule='PROF003',
            nom='Leroy',
            prenom='Sophie',
            email='sophie.leroy@school.fr',
            telephone='0699887766',
            specialite='Français',
            date_embauche=date(2018, 9, 1),
        )
        Matiere.objects.create(
            code_matiere='FR101',
            nom='Littérature',
            coefficient=2.5,
            volume_horaire=50,
            niveau='1ere',
        )
        response = self.client.get(reverse('subjects:dashboard'))
        self.assertContains(response, 'Professeurs')
        self.assertContains(response, 'Matières')


class ProfesseurViewTest(TestCase):
    """Tests pour les vues Professeur."""

    def setUp(self):
        self.client = Client()
        self.professeur = Professeur.objects.create(
            matricule='PROF004',
            nom='Moreau',
            prenom='Pierre',
            email='pierre.moreau@school.fr',
            telephone='0655443322',
            specialite='Histoire',
            date_embauche=date(2017, 9, 1),
        )

    def test_professeur_list_view(self):
        response = self.client.get(reverse('subjects:professeur_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pierre Moreau')

    def test_professeur_detail_view(self):
        response = self.client.get(
            reverse('subjects:professeur_detail', kwargs={'pk': self.professeur.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PROF004')

    def test_professeur_create_view(self):
        response = self.client.post(reverse('subjects:professeur_create'), {
            'matricule': 'PROF005',
            'nom': 'Petit',
            'prenom': 'Luc',
            'email': 'luc.petit@school.fr',
            'telephone': '0610101010',
            'specialite': 'Anglais',
            'date_embauche': '2023-09-01',
            'actif': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Professeur.objects.filter(matricule='PROF005').exists())

    def test_professeur_search(self):
        response = self.client.get(reverse('subjects:professeur_list'), {'q': 'Moreau'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pierre Moreau')


class MatiereViewTest(TestCase):
    """Tests pour les vues Matiere."""

    def setUp(self):
        self.client = Client()
        self.matiere = Matiere.objects.create(
            code_matiere='PHY101',
            nom='Physique générale',
            coefficient=3.5,
            volume_horaire=70,
            niveau='1ere',
        )

    def test_matiere_list_view(self):
        response = self.client.get(reverse('subjects:matiere_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Physique générale')

    def test_matiere_create_view(self):
        response = self.client.post(reverse('subjects:matiere_create'), {
            'code_matiere': 'CHM101',
            'nom': 'Chimie',
            'description': 'Introduction à la chimie',
            'coefficient': '2.5',
            'volume_horaire': 55,
            'niveau': '2eme',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Matiere.objects.filter(code_matiere='CHM101').exists())


class AffectationViewTest(TestCase):
    """Tests pour les vues Affectation."""

    def setUp(self):
        self.client = Client()
        self.professeur = Professeur.objects.create(
            matricule='PROF006',
            nom='Garcia',
            prenom='Ana',
            email='ana.garcia@school.fr',
            telephone='0677889900',
            specialite='Espagnol',
            date_embauche=date(2022, 9, 1),
        )
        self.matiere = Matiere.objects.create(
            code_matiere='ESP101',
            nom='Espagnol',
            coefficient=2.0,
            volume_horaire=40,
            niveau='1ere',
        )
        self.affectation = Affectation.objects.create(
            professeur=self.professeur,
            matiere=self.matiere,
            annee_scolaire='2024-2025',
            semestre=1,
            date_affectation=date(2024, 9, 1),
        )

    def test_affectation_list_view(self):
        response = self.client.get(reverse('subjects:affectation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana Garcia')

    def test_affectation_create_view(self):
        matiere2 = Matiere.objects.create(
            code_matiere='ESP102',
            nom='Espagnol avancé',
            coefficient=3.0,
            volume_horaire=50,
            niveau='2eme',
        )
        response = self.client.post(reverse('subjects:affectation_create'), {
            'professeur': self.professeur.pk,
            'matiere': matiere2.pk,
            'annee_scolaire': '2024-2025',
            'semestre': 2,
            'date_affectation': '2024-09-01',
            'commentaire': 'Affectation test',
            'actif': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Affectation.objects.count(), 2)
