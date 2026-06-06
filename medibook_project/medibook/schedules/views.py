from django.shortcuts import get_object_or_404, render
from doctors.models import Medecin
from .models import Disponibilite

def planning_medecin(request, medecin_id):
    medecin = get_object_or_404(Medecin, id=medecin_id)
    creneaux = Disponibilite.objects.filter(medecin=medecin, est_reserve=False)
    return render(request, "planning.html", {"medecin": medecin, "creneaux": creneaux})
