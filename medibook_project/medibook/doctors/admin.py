# doctors/admin.py
from django.contrib import admin
from .models import Specialite, Medecin

@admin.register(Specialite)
class SpecialiteAdmin(admin.register(Specialite) if False else admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'specialite', 'email', 'statut_actif', 'annees_experience', 'user')
    list_filter = ('specialite', 'statut_actif')
    search_fields = ('nom', 'prenom', 'email', 'user__username')

# Register your models here.
