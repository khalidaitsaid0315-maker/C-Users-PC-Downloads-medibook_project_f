from django.db import models
from appointments.models import RendezVous

class Notification(models.Model):
    TYPE_CHOICES = [('email', 'Email'), ('sms', 'SMS')]
    rendez_vous = models.ForeignKey(RendezVous, on_delete=models.CASCADE, related_name='notifications')
    type_notification = models.CharField(max_length=10, choices=TYPE_CHOICES, default='email')
    message = models.TextField()
    envoye_le = models.DateTimeField(auto_now_add=True)
    statut_succes = models.BooleanField(default=True)

    def __str__(self):
        return f"Notif {self.type_notification} pour RDV #{self.rendez_vous.id} - Statut: {self.statut_succes}"
