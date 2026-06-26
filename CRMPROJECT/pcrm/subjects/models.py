from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Professeur(models.Model):
    """Modèle représentant un professeur de l'établissement."""

    matricule = models.CharField(max_length=20, unique=True, verbose_name='Matricule')
    nom = models.CharField(max_length=100, verbose_name='Nom')
    prenom = models.CharField(max_length=100, verbose_name='Prénom')
    email = models.EmailField(unique=True, verbose_name='Email')
    telephone = models.CharField(max_length=20, verbose_name='Téléphone')
    specialite = models.CharField(max_length=150, verbose_name='Spécialité')
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    actif = models.BooleanField(default=True, verbose_name='Actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Professeur'
        verbose_name_plural = 'Professeurs'
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f'{self.prenom} {self.nom} ({self.matricule})'

    @property
    def nom_complet(self):
        return f'{self.prenom} {self.nom}'


class Matiere(models.Model):
    """Modèle représentant une matière enseignée."""

    NIVEAU_CHOICES = [
        ('1ere', '1ère année'),
        ('2eme', '2ème année'),
        ('3eme', '3ème année'),
        ('4eme', '4ème année'),
        ('5eme', '5ème année'),
    ]

    code_matiere = models.CharField(max_length=20, unique=True, verbose_name='Code matière')
    nom = models.CharField(max_length=150, verbose_name='Nom')
    description = models.TextField(blank=True, verbose_name='Description')
    coefficient = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.5), MaxValueValidator(10)],
        verbose_name='Coefficient',
    )
    volume_horaire = models.PositiveIntegerField(verbose_name='Volume horaire (heures)')
    niveau = models.CharField(max_length=10, choices=NIVEAU_CHOICES, verbose_name='Niveau')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Matière'
        verbose_name_plural = 'Matières'
        ordering = ['niveau', 'nom']

    def __str__(self):
        return f'{self.code_matiere} - {self.nom}'


class Affectation(models.Model):
    """Modèle représentant l'affectation d'un professeur à une matière."""

    SEMESTRE_CHOICES = [
        (1, 'Semestre 1'),
        (2, 'Semestre 2'),
    ]

    professeur = models.ForeignKey(
        Professeur,
        on_delete=models.CASCADE,
        related_name='affectations',
        verbose_name='Professeur',
    )
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name='affectations',
        verbose_name='Matière',
    )
    annee_scolaire = models.CharField(max_length=9, verbose_name='Année scolaire')
    semestre = models.PositiveSmallIntegerField(
        choices=SEMESTRE_CHOICES,
        verbose_name='Semestre',
    )
    date_affectation = models.DateField(verbose_name="Date d'affectation")
    commentaire = models.TextField(blank=True, verbose_name='Commentaire')
    actif = models.BooleanField(default=True, verbose_name='Actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Affectation'
        verbose_name_plural = 'Affectations'
        ordering = ['-annee_scolaire', 'semestre', 'matiere']
        constraints = [
            models.UniqueConstraint(
                fields=['professeur', 'matiere', 'annee_scolaire', 'semestre'],
                name='unique_affectation',
            ),
        ]

    def __str__(self):
        return (
            f'{self.professeur.nom_complet} - {self.matiere.nom} '
            f'({self.annee_scolaire}, S{self.semestre})'
        )

    def clean(self):
        super().clean()
        if not self.annee_scolaire:
            return

        parts = self.annee_scolaire.split('-')
        if len(parts) != 2 or not all(part.isdigit() and len(part) == 4 for part in parts):
            raise ValidationError({
                'annee_scolaire': "Format attendu : AAAA-AAAA (ex: 2024-2025).",
            })

        debut, fin = int(parts[0]), int(parts[1])
        if fin != debut + 1:
            raise ValidationError({
                'annee_scolaire': "L'année de fin doit être l'année de début + 1.",
            })

        if not self.professeur.actif:
            raise ValidationError({
                'professeur': 'Impossible d\'affecter un professeur inactif.',
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
