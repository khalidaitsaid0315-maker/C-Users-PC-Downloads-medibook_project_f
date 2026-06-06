from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PatientSignUpForm


def signup(request):
    if request.method == "POST":
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription reussie. Vous etes connecte(e).")
            return redirect("home")
    else:
        form = PatientSignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
