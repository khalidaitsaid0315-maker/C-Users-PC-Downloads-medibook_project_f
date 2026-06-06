from datetime import date

from django.test import TestCase
from django.urls import reverse

from doctors.models import Specialite
from patients.models import ProfilPatient

from .models import AnalyseSymptome


class AnalyseSymptomeTests(TestCase):
    def setUp(self):
        self.patient = ProfilPatient.objects.create(
            nom="Doe",
            prenom="John",
            email="john@example.com",
            telephone="0603030303",
            date_de_naissance=date(1995, 4, 20),
        )
        Specialite.objects.create(name="Cardiologie")

    def test_orientation_view_creates_analysis(self):
        response = self.client.post(
            reverse("analyser_symptomes"),
            {"texte_symptomes": "J'ai mal a la poitrine avec des palpitations"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(AnalyseSymptome.objects.count(), 1)
        self.assertContains(response, "Cardiologie")
