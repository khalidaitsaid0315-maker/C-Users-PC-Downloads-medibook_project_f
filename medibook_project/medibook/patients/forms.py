from django import forms

from .models import ProfilPatient


class ProfilPatientForm(forms.ModelForm):
    class Meta:
        model = ProfilPatient
        fields = ["nom", "prenom", "email", "telephone", "date_de_naissance"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "date_de_naissance": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
