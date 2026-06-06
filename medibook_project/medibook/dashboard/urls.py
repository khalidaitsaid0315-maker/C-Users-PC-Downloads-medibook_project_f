from django.urls import path
from . import views

urlpatterns = [
    path("", views.global_dashboard, name="global_dashboard"),
]
