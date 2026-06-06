from django.contrib import admin
from .models import Disponibilite

@admin.register(Disponibilite)
class DisponibiliteAdmin(admin.ModelAdmin):
    list_display = ('medecin', 'date', 'heure_debut', 'heure_fin', 'est_reserve')
    list_filter = ('date', 'est_reserve', 'medecin')
    search_fields = ('medecin__nom', 'medecin__prenom')

# Register your models here.
