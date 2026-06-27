from django.db import models

class Specialite(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Profil(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Grade(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Enseignant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    date_recrutement = models.DateField()
    specialite = models.ForeignKey(
        Specialite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    profil = models.ForeignKey(
        Profil,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nom + " " + self.prenom
