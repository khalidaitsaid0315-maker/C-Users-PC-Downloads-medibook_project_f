from django import forms
from .models import RendezVous
from doctors.models import Medecin
from schedules.models import Disponibilite

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ["medecin", "specialite", "date", "heure", "motif"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "heure": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "motif": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Decrivez brievement vos symptomes...",
                }
            ),
            "medecin": forms.Select(attrs={"class": "form-select"}),
            "specialite": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medecin"].queryset = Medecin.objects.filter(statut_actif=True).order_by(
            "nom", "prenom"
        )
        self.fields["specialite"].queryset = self.fields["specialite"].queryset.order_by("name")

    def clean(self):
        cleaned_data = super().clean()
        medecin = cleaned_data.get("medecin")
        date = cleaned_data.get("date")
        heure = cleaned_data.get("heure")

        if medecin and date and heure:
            slot_query = Disponibilite.objects.filter(
                medecin=medecin,
                date=date,
                heure_debut=heure,
            )
            slot = slot_query.filter(est_reserve=False).exists()
            same_instance_slot = False
            if self.instance.pk:
                same_instance_slot = (
                    self.instance.medecin_id == medecin.id
                    and self.instance.date == date
                    and self.instance.heure == heure
                    and slot_query.exists()
                )
            if not slot and not same_instance_slot:
                self.add_error("heure", "Ce creneau n'est pas disponible.")

        return cleaned_data


class RendezVousUpdateForm(RendezVousForm):
    pass
