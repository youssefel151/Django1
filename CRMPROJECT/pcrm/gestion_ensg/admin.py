from django.contrib import admin
from .models import Enseignant, Grade, Profil, Specialite

admin.site.register(Enseignant)
admin.site.register(Specialite)
admin.site.register(Profil)
admin.site.register(Grade)
