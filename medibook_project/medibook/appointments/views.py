from datetime import date as current_date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from notifications.models import Notification
from patients.models import ProfilPatient
from schedules.models import Disponibilite

from .forms import RendezVousForm, RendezVousUpdateForm
from .models import RendezVous


def get_current_patient(request):
    if not request.user.is_authenticated:
        return None

    profile = getattr(request.user, 'patient_profile', None)
    if profile:
        return profile

    email = request.user.email or f"{request.user.username}@medibook.local"
    profile, _ = ProfilPatient.objects.get_or_create(
        user=request.user,
        defaults={
            'nom': request.user.first_name or request.user.username,
            'prenom': request.user.last_name or '',
            'email': email,
            'telephone': '',
            'date_de_naissance': current_date(1970, 1, 1),
        },
    )
    return profile


def sync_slot_status(rendez_vous, reserve):
    Disponibilite.objects.filter(
        medecin=rendez_vous.medecin,
        date=rendez_vous.date,
        heure_debut=rendez_vous.heure,
    ).update(est_reserve=reserve)


def create_notification(rendez_vous, message, notification_type="email"):
    Notification.objects.create(
        rendez_vous=rendez_vous,
        type_notification=notification_type,
        message=message,
    )

@login_required
def reserver_rendezvous(request):
    patient_connecte = get_current_patient(request)

    if request.method == "POST":
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendez_vous = form.save(commit=False)
            rendez_vous.patient = patient_connecte
            rendez_vous.save()
            sync_slot_status(rendez_vous, True)
            create_notification(
                rendez_vous,
                "Votre rendez-vous a bien ete enregistre sur MediBook.",
            )
            messages.success(request, "Le rendez-vous a ete reserve avec succes.")
            return redirect("liste_rendezvous")
    else:
        form = RendezVousForm()

    return render(
        request,
        "appointments/reserver.html",
        {"form": form, "patient": patient_connecte},
    )


@login_required
def liste_rendezvous(request):
    patient = get_current_patient(request)
    rendez_vous = patient.rendez_vous.select_related("medecin", "specialite").order_by(
        "-date", "-heure"
    )
    return render(
        request,
        "appointments/liste.html",
        {"rendez_vous": rendez_vous, "patient": patient},
    )


@login_required
def modifier_rendezvous(request, rendezvous_id):
    patient = get_current_patient(request)
    rendez_vous = get_object_or_404(RendezVous, pk=rendezvous_id)
    if rendez_vous.patient != patient:
        raise Http404()

    old_medecin = rendez_vous.medecin
    old_date = rendez_vous.date
    old_heure = rendez_vous.heure

    if request.method == "POST":
        form = RendezVousUpdateForm(request.POST, instance=rendez_vous)
        if form.is_valid():
            rendez_vous = form.save()
            Disponibilite.objects.filter(
                medecin=old_medecin,
                date=old_date,
                heure_debut=old_heure,
            ).update(est_reserve=False)
            sync_slot_status(rendez_vous, True)
            create_notification(
                rendez_vous,
                "Votre rendez-vous a ete modifie avec succes.",
            )
            messages.success(request, "Le rendez-vous a ete modifie.")
            return redirect("liste_rendezvous")
    else:
        form = RendezVousUpdateForm(instance=rendez_vous)

    return render(
        request,
        "appointments/modifier.html",
        {"form": form, "rendez_vous": rendez_vous},
    )


@login_required
def annuler_rendezvous(request, rendezvous_id):
    patient = get_current_patient(request)
    rendez_vous = get_object_or_404(RendezVous, pk=rendezvous_id)
    if rendez_vous.patient != patient:
        raise Http404()

    if request.method == "POST":
        rendez_vous.statut = "annule"
        rendez_vous.save(update_fields=["statut"])
        sync_slot_status(rendez_vous, False)
        create_notification(
            rendez_vous,
            "Votre rendez-vous a ete annule. Vous pouvez reserver un nouveau creneau.",
        )
        messages.success(request, "Le rendez-vous a ete annule.")
        return redirect("liste_rendezvous")

    return render(
        request,
        "appointments/annuler.html",
        {"rendez_vous": rendez_vous},
    )
