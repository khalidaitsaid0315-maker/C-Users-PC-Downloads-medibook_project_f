from datetime import date, timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Medecin, Specialite


def medecin_list(request):
    q = request.GET.get("q", "").strip()
    specialite_id = request.GET.get("specialite")
    medecins = Medecin.objects.filter(statut_actif=True).select_related("specialite")
    if q:
        medecins = medecins.filter(
            Q(nom__icontains=q)
            | Q(prenom__icontains=q)
            | Q(email__icontains=q)
            | Q(specialite__name__icontains=q)
        )
    if specialite_id:
        medecins = medecins.filter(specialite_id=specialite_id)
    specialites = Specialite.objects.all()
    return render(
        request,
        "medecin_list.html",
        {
            "medecins": medecins,
            "specialites": specialites,
            "query": q,
            "selected_specialite": specialite_id,
        },
    )

def medecin_detail(request, id):
    medecin = get_object_or_404(Medecin, id=id)
    return render(request, "medecin_detail.html", {"medecin": medecin})


def doctor_dashboard(request, medecin_id):
    medecin = get_object_or_404(Medecin, id=medecin_id)
    today = date.today()
    rendez_vous = medecin.rendez_vous.order_by("date", "heure")
    rendez_vous_du_jour = rendez_vous.filter(date=today)
    rendez_vous_semaine = rendez_vous.filter(date__range=[today, today + timedelta(days=7)])
    total_rdv = rendez_vous.count()
    confirms = rendez_vous.filter(statut="confirme").count()
    annules = rendez_vous.filter(statut="annule").count()

    return render(
        request,
        "doctors/doctor_dashboard.html",
        {
            "medecin": medecin,
            "rendez_vous_du_jour": rendez_vous_du_jour,
            "rendez_vous_semaine": rendez_vous_semaine,
            "total_rdv": total_rdv,
            "confirms": confirms,
            "annules": annules,
        },
    )


def specialite_list(request):
    specialites = Specialite.objects.all()
    return render(request, 'doctors/specialite_list.html', {'specialites': specialites})

def specialite_detail(request, id):
    specialite = get_object_or_404(Specialite, id=id)
    medecins = specialite.medecins.filter(statut_actif=True)
    return render(request, 'doctors/specialite_detail.html', {
        'specialite': specialite,
        'medecins': medecins
    })
