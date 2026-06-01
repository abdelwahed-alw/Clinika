from django.urls import path
from . import views

urlpatterns = [
    # Tableau de bord
    path('', views.dashboard, name='dashboard'),

    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/new/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    # Rendez-vous
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/new/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),

    # Agenda
    path('agenda/', views.weekly_agenda, name='weekly_agenda'),

    # Alarmes
    path('alarms/', views.alarm_list, name='alarm_list'),
    path('alarms/<int:pk>/contacted/', views.mark_contacted, name='mark_contacted'),
]
