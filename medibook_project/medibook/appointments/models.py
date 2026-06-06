from django.core.exceptions import ValidationError
from django.db import models
from patients.models import ProfilPatient
from doctors.models import Medecin, Specialite
from schedules.models import Disponibilite

class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
        ('absent', 'Absent'),
    ]

    patient = models.ForeignKey(ProfilPatient, on_delete=models.CASCADE, related_name='rendez_vous')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='rendez_vous')
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, related_name='rendez_vous')
    date = models.DateField()
    heure = models.TimeField()
    motif = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "heure"]
        constraints = [
            models.UniqueConstraint(
                fields=["medecin", "date", "heure"],
                name="unique_rendezvous_medecin_creneau",
            )
        ]

    def clean(self):
        errors = {}

        if self.medecin_id and self.specialite_id and self.medecin.specialite_id != self.specialite_id:
            errors["specialite"] = "La specialite doit correspondre a celle du medecin choisi."

        if self.medecin_id and self.date and self.heure:
            conflit = (
                RendezVous.objects.filter(
                    medecin=self.medecin,
                    date=self.date,
                    heure=self.heure,
                )
                .exclude(pk=self.pk)
                .exclude(statut="annule")
                .exists()
            )
            if conflit:
                errors["heure"] = "Ce creneau est deja reserve pour ce medecin."

            has_slot = Disponibilite.objects.filter(
                medecin=self.medecin,
                date=self.date,
                heure_debut=self.heure,
            ).exists()
            if not has_slot:
                errors["date"] = "Ce rendez-vous doit correspondre a un creneau disponible."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"RDV - {self.patient} avec {self.medecin} le {self.date}"
