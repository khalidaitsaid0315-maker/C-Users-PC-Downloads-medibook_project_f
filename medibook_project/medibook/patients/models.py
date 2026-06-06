from django.contrib.auth.models import User
from django.db import models

class ProfilPatient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="patient_profile",
    )
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    date_de_naissance = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
# Create your models here.
