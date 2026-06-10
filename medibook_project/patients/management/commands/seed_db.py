from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta, time

from patients.models import ProfilPatient
from doctors.models import Medecin, Specialite
from schedules.models import Disponibilite
from appointments.models import RendezVous
from django.contrib.auth.models import User


MOROCCAN_MALE_NAMES = [
    ("Mohammed", "El Idrissi"),
    ("Youssef", "Benjelloun"),
    ("Ahmed", "El Amrani"),
    ("Omar", "Haddad"),
    ("Rachid", "Bouzidi"),
    ("Saad", "Chafik"),
    ("Karim", "Ait Said"),
    ("Mehdi", "El Fassi"),
]

MOROCCAN_FEMALE_NAMES = [
    ("Fatima", "El Idrissi"),
    ("Amina", "Benjelloun"),
    ("Khadija", "El Amrani"),
    ("Salma", "Haddad"),
    ("Nisrine", "Bouzidi"),
    ("Loubna", "Chafik"),
    ("Ilham", "Ait Said"),
    ("Zineb", "El Fassi"),
]


class Command(BaseCommand):
    help = "Seed the database with Moroccan sample data (doctors, patients, slots, appointments)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database with example data...")

        # Specialties
        specialites = [
            ("Generaliste", "Médecin généraliste pour consultations courantes"),
            ("Dermatologie", "Soins de la peau"),
            ("Pediatrie", "Soins des enfants"),
            ("Cardiologie", "Cœur et circulation"),
            ("Gynecologie", "Santé des femmes"),
        ]

        spec_objs = []
        for name, desc in specialites:
            spec, _ = Specialite.objects.get_or_create(name=name, defaults={"description": desc})
            spec_objs.append(spec)

        # Create doctors
        doctors_data = [
            ("Mohammed", "El Idrissi", "mohammed.elidrissi@example.com", "0600000001", spec_objs[0]),
            ("Youssef", "Benjelloun", "youssef.benjelloun@example.com", "0600000002", spec_objs[1]),
            ("Amina", "Benjelloun", "amina.benjelloun@example.com", "0600000003", spec_objs[2]),
            ("Karim", "Ait Said", "karim.aitsaid@example.com", "0600000004", spec_objs[3]),
            ("Fatima", "El Fassi", "fatima.elfassi@example.com", "0600000005", spec_objs[4]),
        ]

        medecins = []
        for nom, prenom, email, tel, specialite in doctors_data:
            med, created = Medecin.objects.get_or_create(
                email=email,
                defaults={
                    "nom": nom,
                    "prenom": prenom,
                    "telephone_professionnel": tel,
                    "specialite": specialite,
                    "adresse_cabinet": f"Rue Principale, Casablanca",
                    "description": f"Dr. {nom} {prenom}, spécialiste en {specialite.name}",
                    "annees_experience": 5,
                    "statut_actif": True,
                },
            )
            medecins.append(med)

        # Create patients
        patients = []
        sample_patients = MOROCCAN_MALE_NAMES[:5] + MOROCCAN_FEMALE_NAMES[:5]
        for i, (prenom, nom) in enumerate(sample_patients, start=1):
            email = f"{prenom.lower()}.{nom.lower().replace(' ', '')}.{i}@example.com"
            patient, created = ProfilPatient.objects.get_or_create(
                email=email,
                defaults={
                    "nom": nom,
                    "prenom": prenom,
                    "telephone": f"06{1000000 + i}",
                    "date_de_naissance": date(1990 + (i % 10), 1 + (i % 12), 1 + (i % 27)),
                },
            )
            patients.append(patient)

        # Create disponibilites for next 7 days for each medecin (09:00,10:00,11:00,14:00,15:00)
        start_date = date.today() + timedelta(days=1)
        for med in medecins:
            for d in range(7):
                day = start_date + timedelta(days=d)
                for hour in (9, 10, 11, 14, 15):
                    hstart = time(hour, 0)
                    Disponibilite.objects.get_or_create(
                        medecin=med,
                        date=day,
                        heure_debut=hstart,
                        heure_fin=time(hour, 50),
                    )

        # Create a few appointments using available slots
        created_rv = 0
        for idx, patient in enumerate(patients[:6]):
            med = medecins[idx % len(medecins)]
            # find a disponibilite not reserved
            slot = Disponibilite.objects.filter(medecin=med, est_reserve=False).order_by("date", "heure_debut").first()
            if slot:
                rv = RendezVous.objects.create(
                    patient=patient,
                    medecin=med,
                    specialite=med.specialite,
                    date=slot.date,
                    heure=slot.heure_debut,
                    motif="Consultation de routine",
                    statut="confirme",
                )
                slot.est_reserve = True
                slot.save()
                created_rv += 1

        self.stdout.write(self.style.SUCCESS(f"Created {len(spec_objs)} specialities, {len(medecins)} medecins, {len(patients)} patients, and {created_rv} rendez-vous."))
