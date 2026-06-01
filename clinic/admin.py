from django.contrib import admin
from .models import Patient, Appointment


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'last_name', 'first_name', 'date_of_birth',
        'phone', 'blood_group', 'city', 'created_at',
    )
    list_filter = ('blood_group', 'city', 'created_at')
    search_fields = ('last_name', 'first_name', 'cin', 'phone', 'email')
    ordering = ('-created_at',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'date_time', 'type', 'status',
        'contacted_for_reminder',
    )
    list_filter = ('status', 'type', 'date_time', 'contacted_for_reminder')
    search_fields = (
        'patient__last_name', 'patient__first_name', 'reason',
    )
    ordering = ('date_time',)
