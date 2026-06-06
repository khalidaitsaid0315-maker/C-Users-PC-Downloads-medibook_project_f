from django.db import models
from doctors.models import Medecin

class Disponibilite(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='disponibilites')
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    est_reserve = models.BooleanField(default=False)

    class Meta:
        ordering = ["date", "heure_debut"]
        constraints = [
            models.UniqueConstraint(
                fields=["medecin", "date", "heure_debut"],
                name="unique_disponibilite_medecin_creneau",
            )
        ]

    def __str__(self):
        statut = "Réservé" if self.est_reserve else "Libre"
        return f"Dr. {self.medecin.nom} - {self.date} ({self.heure_debut} - {self.heure_fin}) [{statut}]"
