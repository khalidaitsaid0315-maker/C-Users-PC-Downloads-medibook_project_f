from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfilPatientForm
from .models import ProfilPatient


def patient_list(request):
    patients = ProfilPatient.objects.all().order_by("nom", "prenom")
    return render(request, "patients/liste.html", {"patients": patients})


def patient_detail(request, patient_id):
    patient = get_object_or_404(ProfilPatient, pk=patient_id)
    historique = patient.rendez_vous.select_related("medecin", "specialite").order_by(
        "-date", "-heure"
    )
    return render(
        request,
        "patients/detail.html",
        {"patient": patient, "historique": historique},
    )


@login_required
def patient_dashboard(request):
    profile = get_object_or_404(ProfilPatient, user=request.user)
    today = date.today()
    rendez_vous = profile.rendez_vous.select_related("medecin", "specialite")
    prochains = rendez_vous.filter(date__gte=today).order_by("date", "heure")
    passes = rendez_vous.filter(date__lt=today).order_by("-date", "-heure")
    annules = rendez_vous.filter(statut="annule").order_by("-date", "-heure")

    return render(
        request,
        "patients/dashboard.html",
        {
            "patient": profile,
            "prochains": prochains,
            "passes": passes,
            "annules": annules,
        },
    )


@login_required
def modifier_profil(request):
    profile = get_object_or_404(ProfilPatient, user=request.user)
    if request.method == "POST":
        form = ProfilPatientForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a ete mis a jour avec succes.")
            return redirect("patient_dashboard")
    else:
        form = ProfilPatientForm(instance=profile)
    return render(request, "patients/edit_profile.html", {"form": form})
