from django.shortcuts import render
from .models import Notification

def liste_notifications(request):
    notifications = Notification.objects.select_related(
        "rendez_vous", "rendez_vous__patient", "rendez_vous__medecin"
    ).order_by("-envoye_le")
    return render(request, "liste.html", {"notifications": notifications})
