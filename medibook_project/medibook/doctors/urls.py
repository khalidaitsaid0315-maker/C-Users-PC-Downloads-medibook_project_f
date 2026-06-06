from django.urls import path
from . import views

urlpatterns = [
    path('', views.medecin_list, name='medecin_list'),
    path('<int:id>/', views.medecin_detail, name='medecin_detail'),
    path('<int:medecin_id>/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('specialites/', views.specialite_list, name='specialite_list'),
    path('specialite/<int:id>/', views.specialite_detail, name='specialite_detail'),
]
