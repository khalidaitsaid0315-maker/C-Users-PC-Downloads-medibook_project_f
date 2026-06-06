from django.db.models import Count
from django.shortcuts import render
from doctors.models import Medecin
from patients.models import ProfilPatient
from appointments.models import RendezVous

def global_dashboard(request):
    total_medecins = Medecin.objects.count()
    total_patients = ProfilPatient.objects.count()
    total_rdv = RendezVous.objects.count()
    rdv_en_attente = RendezVous.objects.filter(statut='en_attente').count()
    rdv_confirmes = RendezVous.objects.filter(statut="confirme").count()
    rdv_annules = RendezVous.objects.filter(statut="annule").count()
    rdv_par_specialite = (
        RendezVous.objects.values("specialite__name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )
    rdv_par_medecin = (
        RendezVous.objects.values("medecin__nom", "medecin__prenom")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    context = {
        "total_medecins": total_medecins,
        "total_patients": total_patients,
        "total_rdv": total_rdv,
        "rdv_en_attente": rdv_en_attente,
        "rdv_confirmes": rdv_confirmes,
        "rdv_annules": rdv_annules,
        "rdv_par_specialite": rdv_par_specialite,
        "rdv_par_medecin": rdv_par_medecin,
    }
    return render(request, "home.html", context)
