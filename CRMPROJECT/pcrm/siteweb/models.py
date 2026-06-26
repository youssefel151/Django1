from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_ENSEIGNANT = 'enseignant'
    ROLE_ETUDIANT = 'etudiant'

    ROLE_CHOICES = [
        (ROLE_ENSEIGNANT, 'Enseignant'),
        (ROLE_ETUDIANT, 'Etudiant'),
        (ROLE_ADMIN, 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_ETUDIANT)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    student_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Niveau(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Parcours(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='parcours')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['niveau__nom', 'nom']
        unique_together = ('nom', 'niveau')

    def __str__(self):
        return f"{self.nom} ({self.niveau})"


class Groupe(models.Model):
    nom = models.CharField(max_length=100)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='groupes')
    parcours = models.ForeignKey(
        Parcours,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='groupes',
    )
    capacite = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ['niveau__nom', 'parcours__nom', 'nom']
        unique_together = ('nom', 'niveau', 'parcours')

    def __str__(self):
        return f"{self.nom} - {self.niveau}"


class Record(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    zipcode=models.CharField(max_length=20)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")


class Etudiant(models.Model):
    FILIERE_CHOICES = [
        ('Marketing Digital', 'Marketing Digital et Data Analytics'),
        ('Commerce International', 'Commerce International'),
        ('Management', 'Management Global'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    filiere = models.CharField(max_length=100, choices=FILIERE_CHOICES, default='Marketing Digital')
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    matiere = models.CharField(max_length=100)
    valeur = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(20.0)])
    date_saisie = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['etudiant__nom', 'matiere']
        unique_together = ('etudiant', 'matiere')

    def __str__(self):
        return f"{self.etudiant} - {self.matiere} : {self.valeur}/20"
