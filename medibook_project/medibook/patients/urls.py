from django.urls import path

from . import views

urlpatterns = [
    path("", views.patient_list, name="patient_list"),
    path("<int:patient_id>/", views.patient_detail, name="patient_detail"),
    path("dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("dashboard/profil/modifier/", views.modifier_profil, name="modifier_profil"),
]
