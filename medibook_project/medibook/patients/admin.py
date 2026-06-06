# patients/admin.py
from django.contrib import admin
from .models import ProfilPatient

@admin.register(ProfilPatient)
class ProfilPatientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'user')
    search_fields = ('nom', 'prenom', 'email', 'user__username')
