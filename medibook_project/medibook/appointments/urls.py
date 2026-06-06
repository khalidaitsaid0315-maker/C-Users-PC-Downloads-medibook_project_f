from django.urls import path
from . import views

urlpatterns = [
    path("", views.liste_rendezvous, name="liste_rendezvous"),
    path("reserver/", views.reserver_rendezvous, name="reserver_rendezvous"),
    path("<int:rendezvous_id>/modifier/", views.modifier_rendezvous, name="modifier_rendezvous"),
    path("<int:rendezvous_id>/annuler/", views.annuler_rendezvous, name="annuler_rendezvous"),
]
