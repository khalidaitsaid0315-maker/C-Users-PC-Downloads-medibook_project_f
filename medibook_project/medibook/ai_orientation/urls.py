from django.urls import path
from . import views

urlpatterns = [
    path("", views.analyser_symptomes, name="analyser_symptomes"),
    path('historique/', views.historique_ia, name='historique_ia'),
]
