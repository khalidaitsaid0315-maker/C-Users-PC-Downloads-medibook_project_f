from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from patients.models import ProfilPatient


class PatientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    nom = forms.CharField(max_length=100, required=True, label="Nom")
    prenom = forms.CharField(max_length=100, required=True, label="Prenom")
    telephone = forms.CharField(max_length=20, required=True, label="Telephone")
    date_de_naissance = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date de naissance",
    )

    class Meta:
        model = User
        fields = ["username", "email", "nom", "prenom", "telephone", "date_de_naissance", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["nom"]
        user.last_name = self.cleaned_data["prenom"]
        if commit:
            user.save()
            ProfilPatient.objects.create(
                user=user,
                nom=self.cleaned_data["nom"],
                prenom=self.cleaned_data["prenom"],
                email=self.cleaned_data["email"],
                telephone=self.cleaned_data["telephone"],
                date_de_naissance=self.cleaned_data["date_de_naissance"],
            )
        return user
