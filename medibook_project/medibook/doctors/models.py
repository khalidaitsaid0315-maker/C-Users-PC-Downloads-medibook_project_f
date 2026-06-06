from django.contrib.auth.models import User
from django.db import models

class Specialite(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Medecin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medecin_profile',
    )
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone_professionnel = models.CharField(max_length=20)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, related_name='medecins')
    adresse_cabinet = models.TextField()
    description = models.TextField(blank=True)
    annees_experience = models.PositiveSmallIntegerField(default=0)
    statut_actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='doctors/photos/', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.nom} {self.prenom} ({self.specialite.name})"
# Create your models here.
