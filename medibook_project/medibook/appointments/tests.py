from datetime import date, time

from django.test import TestCase

from doctors.models import Medecin, Specialite
from patients.models import ProfilPatient
from schedules.models import Disponibilite

from .forms import RendezVousForm
from .models import RendezVous


class RendezVousFormTests(TestCase):
    def setUp(self):
        self.specialite = Specialite.objects.create(name="Cardiologie")
        self.medecin = Medecin.objects.create(
            nom="House",
            prenom="Gregory",
            email="house@example.com",
            telephone_professionnel="0601010101",
            specialite=self.specialite,
            adresse_cabinet="Hopital central",
        )
        self.patient = ProfilPatient.objects.create(
            nom="Doe",
            prenom="Jane",
            email="jane@example.com",
            telephone="0602020202",
            date_de_naissance=date(1998, 1, 1),
        )
        self.creneau = Disponibilite.objects.create(
            medecin=self.medecin,
            date=date(2026, 5, 30),
            heure_debut=time(10, 0),
            heure_fin=time(10, 30),
        )

    def test_form_is_valid_when_slot_is_available(self):
        form = RendezVousForm(
            data={
                "medecin": self.medecin.id,
                "specialite": self.specialite.id,
                "date": "2026-05-30",
                "heure": "10:00",
                "motif": "Controle annuel",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_when_slot_is_reserved(self):
        RendezVous.objects.create(
            patient=self.patient,
            medecin=self.medecin,
            specialite=self.specialite,
            date=date(2026, 5, 30),
            heure=time(10, 0),
            motif="Premier rendez-vous",
        )
        self.creneau.est_reserve = True
        self.creneau.save(update_fields=["est_reserve"])

        form = RendezVousForm(
            data={
                "medecin": self.medecin.id,
                "specialite": self.specialite.id,
                "date": "2026-05-30",
                "heure": "10:00",
                "motif": "Second rendez-vous",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("heure", form.errors)
