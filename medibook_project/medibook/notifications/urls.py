from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_notifications, name='liste_notifications'),
]
