import re
from datetime import date, timedelta, time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from ai_orientation.models import AnalyseSymptome
from appointments.models import RendezVous
from doctors.models import Medecin, Specialite
from notifications.models import Notification
from patients.models import ProfilPatient
from schedules.models import Disponibilite


DEMO_DOMAIN = "demo.medibook.ma"
DEMO_PASSWORD = "MediBook@2026"

SPECIALITES = [
    ("Medecine generale", "Consultations courantes, suivi medical, prevention et orientation."),
    ("Cardiologie", "Diagnostic et suivi des maladies du coeur, tension et circulation."),
    ("Dermatologie", "Soins de la peau, allergies, acne, eczema et lesions cutanees."),
    ("Pediatrie", "Suivi medical des enfants, nourrissons, vaccins et croissance."),
    ("Gynecologie", "Sante de la femme, suivi gynecologique et consultations de grossesse."),
    ("Neurologie", "Migraines, vertiges, troubles neurologiques et suivi du systeme nerveux."),
    ("Ophtalmologie", "Vision, douleurs oculaires, lunettes, larmoiement et suivi des yeux."),
    ("ORL", "Oreilles, nez, gorge, sinus, audition et troubles de la voix."),
    ("Dentisterie", "Soins dentaires, detartrage, douleurs dentaires et prevention bucco-dentaire."),
    ("Orthopedie", "Os, articulations, fractures, douleurs du dos et traumatologie."),
    ("Psychiatrie", "Sante mentale, anxiete, sommeil, humeur et accompagnement psychologique."),
    ("Endocrinologie", "Diabete, thyroide, hormones, nutrition et troubles metabolique."),
]

DOCTORS = [
    {
        "first_name": "Youssef",
        "last_name": "El Amrani",
        "email": "dr.youssef.elamrani@demo.medibook.ma",
        "phone": "0522000101",
        "specialite": "Cardiologie",
        "city": "Casablanca",
        "address": "45 boulevard Zerktouni, Casablanca",
        "experience": 14,
    },
    {
        "first_name": "Salma",
        "last_name": "Benjelloun",
        "email": "dr.salma.benjelloun@demo.medibook.ma",
        "phone": "0537000102",
        "specialite": "Dermatologie",
        "city": "Rabat",
        "address": "12 avenue Annakhil, Rabat",
        "experience": 9,
    },
    {
        "first_name": "Karim",
        "last_name": "Ait Taleb",
        "email": "dr.karim.aittaleb@demo.medibook.ma",
        "phone": "0524000103",
        "specialite": "Pediatrie",
        "city": "Marrakech",
        "address": "18 rue Ibn Sina, Marrakech",
        "experience": 11,
    },
    {
        "first_name": "Amina",
        "last_name": "El Fassi",
        "email": "dr.amina.elfassi@demo.medibook.ma",
        "phone": "0535000104",
        "specialite": "Gynecologie",
        "city": "Fes",
        "address": "7 avenue Hassan II, Fes",
        "experience": 16,
    },
    {
        "first_name": "Mehdi",
        "last_name": "Bennis",
        "email": "dr.mehdi.bennis@demo.medibook.ma",
        "phone": "0539000105",
        "specialite": "Neurologie",
        "city": "Tanger",
        "address": "31 boulevard Pasteur, Tanger",
        "experience": 8,
    },
    {
        "first_name": "Nadia",
        "last_name": "Chraibi",
        "email": "dr.nadia.chraibi@demo.medibook.ma",
        "phone": "0522000106",
        "specialite": "Ophtalmologie",
        "city": "Casablanca",
        "address": "21 rue Socrate, Casablanca",
        "experience": 12,
    },
    {
        "first_name": "Othmane",
        "last_name": "Alaoui",
        "email": "dr.othmane.alaoui@demo.medibook.ma",
        "phone": "0537000107",
        "specialite": "ORL",
        "city": "Rabat",
        "address": "5 avenue Fal Ould Oumeir, Rabat",
        "experience": 10,
    },
    {
        "first_name": "Laila",
        "last_name": "Bennani",
        "email": "dr.laila.bennani@demo.medibook.ma",
        "phone": "0528000108",
        "specialite": "Dentisterie",
        "city": "Agadir",
        "address": "9 avenue des FAR, Agadir",
        "experience": 7,
    },
    {
        "first_name": "Hamza",
        "last_name": "Tazi",
        "email": "dr.hamza.tazi@demo.medibook.ma",
        "phone": "0535000109",
        "specialite": "Orthopedie",
        "city": "Meknes",
        "address": "27 avenue Mohammed V, Meknes",
        "experience": 15,
    },
    {
        "first_name": "Imane",
        "last_name": "Skalli",
        "email": "dr.imane.skalli@demo.medibook.ma",
        "phone": "0522000110",
        "specialite": "Psychiatrie",
        "city": "Casablanca",
        "address": "16 boulevard Ghandi, Casablanca",
        "experience": 13,
    },
    {
        "first_name": "Reda",
        "last_name": "El Malki",
        "email": "dr.reda.elmalki@demo.medibook.ma",
        "phone": "0536000111",
        "specialite": "Endocrinologie",
        "city": "Oujda",
        "address": "14 boulevard Allal El Fassi, Oujda",
        "experience": 6,
    },
    {
        "first_name": "Sara",
        "last_name": "El Khatib",
        "email": "dr.sara.elkhatib@demo.medibook.ma",
        "phone": "0537000112",
        "specialite": "Medecine generale",
        "city": "Kenitra",
        "address": "22 avenue Mohamed Diouri, Kenitra",
        "experience": 5,
    },
]

PATIENTS = [
    ("Mohammed", "Berrada", "mohammed.berrada@demo.medibook.ma", "0611000101", date(1984, 3, 12)),
    ("Fatima", "El Idrissi", "fatima.elidrissi@demo.medibook.ma", "0611000102", date(1991, 7, 4)),
    ("Yassine", "Ouazzani", "yassine.ouazzani@demo.medibook.ma", "0611000103", date(1978, 11, 20)),
    ("Amina", "Ait Lahcen", "amina.aitlahcen@demo.medibook.ma", "0611000104", date(1996, 1, 18)),
    ("Hamza", "Benali", "hamza.benali@demo.medibook.ma", "0611000105", date(2001, 5, 9)),
    ("Khadija", "Mansouri", "khadija.mansouri@demo.medibook.ma", "0611000106", date(1969, 9, 25)),
    ("Omar", "Chraibi", "omar.chraibi@demo.medibook.ma", "0611000107", date(1988, 12, 2)),
    ("Zineb", "Bennani", "zineb.bennani@demo.medibook.ma", "0611000108", date(1993, 6, 15)),
    ("Rania", "El Moutawakil", "rania.elmoutawakil@demo.medibook.ma", "0611000109", date(2007, 4, 8)),
    ("Ayoub", "Fadili", "ayoub.fadili@demo.medibook.ma", "0611000110", date(1999, 10, 31)),
    ("Salma", "Lamrani", "salma.lamrani@demo.medibook.ma", "0611000111", date(1982, 8, 13)),
    ("Noureddine", "Tazi", "noureddine.tazi@demo.medibook.ma", "0611000112", date(1974, 2, 27)),
    ("Hajar", "El Kabbaj", "hajar.elkabbaj@demo.medibook.ma", "0611000113", date(1995, 12, 6)),
    ("Ilyas", "Alaoui", "ilyas.alaoui@demo.medibook.ma", "0611000114", date(2012, 6, 19)),
    ("Meryem", "Skalli", "meryem.skalli@demo.medibook.ma", "0611000115", date(1986, 5, 24)),
    ("Adil", "Belkadi", "adil.belkadi@demo.medibook.ma", "0611000116", date(1990, 3, 3)),
    ("Nawal", "Bouzidi", "nawal.bouzidi@demo.medibook.ma", "0611000117", date(1972, 7, 22)),
    ("Anas", "Rami", "anas.rami@demo.medibook.ma", "0611000118", date(2004, 9, 14)),
    ("Siham", "El Gharbi", "siham.elgharbi@demo.medibook.ma", "0611000119", date(1981, 1, 30)),
    ("Taha", "Bennis", "taha.bennis@demo.medibook.ma", "0611000120", date(1997, 11, 11)),
    ("Malak", "El Fassi", "malak.elfassi@demo.medibook.ma", "0611000121", date(2009, 2, 16)),
    ("Rachid", "Mernissi", "rachid.mernissi@demo.medibook.ma", "0611000122", date(1965, 10, 5)),
    ("Ilham", "Tahiri", "ilham.tahiri@demo.medibook.ma", "0611000123", date(1994, 4, 21)),
    ("Soufiane", "Boulahrouz", "soufiane.boulahrouz@demo.medibook.ma", "0611000124", date(1989, 6, 7)),
]

MOTIFS = [
    "Controle medical de routine",
    "Douleur thoracique et fatigue",
    "Boutons et irritation de la peau",
    "Suivi pediatrique et vaccination",
    "Consultation de suivi gynecologique",
    "Migraines frequentes",
    "Vision trouble en fin de journee",
    "Douleur de gorge persistante",
    "Douleur dentaire",
    "Douleur au genou apres effort",
    "Troubles du sommeil et anxiete",
    "Controle du diabete",
]

AI_ANALYSES = [
    ("Douleur dans la poitrine avec palpitations et tension elevee", "Cardiologie", 86.0),
    ("Rougeurs sur la peau avec boutons et allergie depuis trois jours", "Dermatologie", 78.0),
    ("Enfant avec fievre legere et toux depuis hier", "Pediatrie", 74.0),
    ("Migraine forte, vertige et douleur a la tete", "Neurologie", 82.0),
    ("Vision floue, oeil rouge et larmoiement", "Ophtalmologie", 80.0),
    ("Fatigue, soif frequente et controle du diabete", "Endocrinologie", 69.0),
]


class Command(BaseCommand):
    help = "Seed the database with Moroccan demo data for MediBook."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default=DEMO_PASSWORD,
            help="Password set for all demo users.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.password = options["password"]
        today = date.today()

        specialites = self.create_specialites()
        doctors = self.create_doctors(specialites)
        patients = self.create_patients()
        slot_count = self.create_slots(doctors, today)
        rendez_vous = self.create_appointments(doctors, patients, today)
        notification_count = self.create_notifications(rendez_vous)
        analysis_count = self.create_ai_analyses(patients, specialites)
        self.sync_slot_reservations(doctors, today)

        self.stdout.write(
            self.style.SUCCESS(
                "Seed termine: "
                f"{len(specialites)} specialites, "
                f"{len(doctors)} medecins, "
                f"{len(patients)} patients, "
                f"{slot_count} creneaux, "
                f"{len(rendez_vous)} rendez-vous, "
                f"{notification_count} notifications, "
                f"{analysis_count} analyses IA."
            )
        )
        self.stdout.write(
            "Comptes demo: patient.mohammed.berrada, dr.youssef.elamrani "
            f"(mot de passe: {self.password})"
        )

    def create_specialites(self):
        specialites = {}
        for name, description in SPECIALITES:
            specialite, _ = Specialite.objects.update_or_create(
                name=name,
                defaults={"description": description},
            )
            specialites[name] = specialite
        return specialites

    def create_doctors(self, specialites):
        doctors = []
        for data in DOCTORS:
            user = self.create_demo_user(
                username=self.username_from_email(data["email"]),
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            specialite = specialites[data["specialite"]]
            doctor, _ = Medecin.objects.update_or_create(
                email=data["email"],
                defaults={
                    "user": user,
                    "nom": data["last_name"],
                    "prenom": data["first_name"],
                    "telephone_professionnel": data["phone"],
                    "specialite": specialite,
                    "adresse_cabinet": data["address"],
                    "description": (
                        f"Dr. {data['first_name']} {data['last_name']} exerce a "
                        f"{data['city']} en {specialite.name}."
                    ),
                    "annees_experience": data["experience"],
                    "statut_actif": True,
                },
            )
            doctors.append(doctor)
        return doctors

    def create_patients(self):
        patients = []
        for first_name, last_name, email, phone, birth_date in PATIENTS:
            user = self.create_demo_user(
                username=self.username_from_email(email),
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            patient, _ = ProfilPatient.objects.get_or_create(
                email=email,
                defaults={
                    "nom": last_name,
                    "prenom": first_name,
                    "telephone": phone,
                    "date_de_naissance": birth_date,
                },
            )
            patient.nom = last_name
            patient.prenom = first_name
            patient.telephone = phone
            patient.date_de_naissance = birth_date
            if not ProfilPatient.objects.filter(user=user).exclude(pk=patient.pk).exists():
                patient.user = user
            patient.save()
            patients.append(patient)
        return patients

    def create_slots(self, doctors, today):
        slot_count = 0
        start_day = today - timedelta(days=7)
        end_day = today + timedelta(days=21)
        day_count = (end_day - start_day).days + 1

        for doctor in doctors:
            for offset in range(day_count):
                slot_day = start_day + timedelta(days=offset)
                if slot_day.weekday() == 6:
                    continue

                hours = (9, 10, 11, 14, 15, 16)
                if slot_day.weekday() == 5:
                    hours = (9, 10, 11, 12)

                for hour in hours:
                    slot, created = Disponibilite.objects.get_or_create(
                        medecin=doctor,
                        date=slot_day,
                        heure_debut=time(hour, 0),
                        defaults={"heure_fin": time(hour, 50)},
                    )
                    if not created and slot.heure_fin != time(hour, 50):
                        slot.heure_fin = time(hour, 50)
                        slot.save(update_fields=["heure_fin"])
                    slot_count += 1
        return slot_count

    def create_appointments(self, doctors, patients, today):
        past_slots = list(
            Disponibilite.objects.filter(medecin__in=doctors, date__lt=today)
            .select_related("medecin", "medecin__specialite")
            .order_by("date", "heure_debut", "medecin__email")
        )
        future_slots = list(
            Disponibilite.objects.filter(medecin__in=doctors, date__gte=today)
            .select_related("medecin", "medecin__specialite")
            .order_by("date", "heure_debut", "medecin__email")
        )
        selected_slots = self.pick_spread(past_slots, 14) + self.pick_spread(future_slots, 26)
        past_statuses = ("termine", "termine", "absent", "annule")
        future_statuses = ("confirme", "confirme", "en_attente", "annule")
        appointments = []

        for index, slot in enumerate(selected_slots):
            patient = patients[index % len(patients)]
            status_choices = past_statuses if slot.date < today else future_statuses
            status = status_choices[index % len(status_choices)]
            motif = MOTIFS[index % len(MOTIFS)]

            existing = (
                RendezVous.objects.filter(
                    medecin=slot.medecin,
                    date=slot.date,
                    heure=slot.heure_debut,
                )
                .select_related("patient")
                .first()
            )
            if existing:
                if not existing.patient.email.endswith(f"@{DEMO_DOMAIN}"):
                    continue
                existing.patient = patient
                existing.specialite = slot.medecin.specialite
                existing.motif = motif
                existing.statut = status
                existing.save()
                appointment = existing
            else:
                appointment = RendezVous.objects.create(
                    patient=patient,
                    medecin=slot.medecin,
                    specialite=slot.medecin.specialite,
                    date=slot.date,
                    heure=slot.heure_debut,
                    motif=motif,
                    statut=status,
                )
            appointments.append(appointment)
        return appointments

    def create_notifications(self, appointments):
        messages = {
            "en_attente": "Votre demande de rendez-vous est en attente de confirmation.",
            "confirme": "Votre rendez-vous MediBook est confirme.",
            "annule": "Votre rendez-vous MediBook a ete annule.",
            "termine": "Merci pour votre visite. Votre rendez-vous est marque comme termine.",
            "absent": "Vous avez manque votre rendez-vous MediBook.",
        }
        notification_count = 0
        for appointment in appointments:
            message = messages[appointment.statut]
            _, created = Notification.objects.get_or_create(
                rendez_vous=appointment,
                type_notification="email",
                message=message,
                defaults={"statut_succes": appointment.statut != "absent"},
            )
            notification_count += 1
            if appointment.statut in {"confirme", "en_attente"}:
                _, sms_created = Notification.objects.get_or_create(
                    rendez_vous=appointment,
                    type_notification="sms",
                    message=message,
                    defaults={"statut_succes": True},
                )
                if sms_created:
                    notification_count += 1
        return notification_count

    def create_ai_analyses(self, patients, specialites):
        analysis_count = 0
        for index, (text, specialite_name, score) in enumerate(AI_ANALYSES):
            patient = patients[index % len(patients)]
            _, created = AnalyseSymptome.objects.get_or_create(
                patient=patient,
                texte_symptomes=text,
                specialite_recommandee=specialites[specialite_name],
                defaults={"score_confiance": score},
            )
            if created:
                analysis_count += 1
        return analysis_count

    def sync_slot_reservations(self, doctors, today):
        start_day = today - timedelta(days=7)
        end_day = today + timedelta(days=21)
        slots = Disponibilite.objects.filter(
            medecin__in=doctors,
            date__range=(start_day, end_day),
        )
        for slot in slots:
            reserved = (
                RendezVous.objects.filter(
                    medecin=slot.medecin,
                    date=slot.date,
                    heure=slot.heure_debut,
                )
                .exclude(statut="annule")
                .exists()
            )
            if slot.est_reserve != reserved:
                slot.est_reserve = reserved
                slot.save(update_fields=["est_reserve"])

    def create_demo_user(self, username, email, first_name, last_name):
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
            },
        )
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.set_password(self.password)
        user.save()
        return user

    @staticmethod
    def username_from_email(email):
        username = email.split("@", 1)[0]
        username = re.sub(r"[^a-zA-Z0-9_.-]+", ".", username).strip(".")
        return username.lower()

    @staticmethod
    def pick_spread(slots, count):
        if not slots or count <= 0:
            return []
        if len(slots) <= count:
            return slots
        step = max(len(slots) // count, 1)
        selected = slots[::step][:count]
        return selected
