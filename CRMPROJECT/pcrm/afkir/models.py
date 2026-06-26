from django.db import models

class Etudiant(models.Model):
    code_massar = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    date_naissance = models.DateField()

    def __str__(self):
        return f'{self.nom} {self.prenom}'

class Inscription(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    filiere = models.CharField(max_length=100)
    date_inscription = models.DateField(auto_now_add=True)
    niveau = models.CharField(max_length=20)
    statut = models.CharField(max_length=20, default='Valide')

    def __str__(self):
        return f'Inscription de {self.etudiant} en {self.filiere}'
