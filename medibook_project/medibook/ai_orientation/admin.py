from django.contrib import admin
from .models import AnalyseSymptome

@admin.register(AnalyseSymptome)
class AnalyseSymptomeAdmin(admin.ModelAdmin):
    list_display = ('patient', 'specialite_recommandee', 'score_confiance', 'cree_le')
    list_filter = ('specialite_recommandee',)

# Register your models here.
