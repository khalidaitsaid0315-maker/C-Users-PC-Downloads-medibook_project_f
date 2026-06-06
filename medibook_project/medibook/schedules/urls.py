from django.urls import path
from . import views

urlpatterns = [
    path("medecin/<int:medecin_id>/", views.planning_medecin, name="planning_medecin"),
]
