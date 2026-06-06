from django.db import models
from patients.models import ProfilPatient
from doctors.models import Specialite

class AnalyseSymptome(models.Model):
    patient = models.ForeignKey(ProfilPatient, on_delete=models.CASCADE, null=True, blank=True)
    texte_symptomes = models.TextField()
    specialite_recommandee = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True)
    score_confiance = models.FloatField(default=0.0) # Score du calcul TF-IDF
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analyse #{self.id} -> Recommandation: {self.specialite_recommandee}"

# Create your models here.
