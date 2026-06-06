# appointments/admin.py
from django.contrib import admin
from .models import RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date', 'heure', 'statut')
    list_filter = ('statut', 'date')
    search_fields = ('patient__nom', 'medecin__nom', 'motif')

# Register your models here.
