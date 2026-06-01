from datetime import timedelta
from itertools import groupby

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .models import Patient, Appointment
from .forms import PatientForm, AppointmentForm


# ───────────────────────────────────────────
# 1. Tableau de bord (Dashboard)
# ───────────────────────────────────────────

def dashboard(request):
    """Main dashboard view."""
    today = timezone.localdate()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Statistiques
    total_patients_today = Patient.objects.filter(
        created_at__date=today,
    ).count()
    total_appointments_today = Appointment.objects.filter(
        date_time__date=today,
    ).count()
    total_appointments_week = Appointment.objects.filter(
        date_time__date__gte=start_of_week,
        date_time__date__lte=end_of_week,
    ).count()

    # Alarmes
    pending_alarms = Appointment.objects.get_pending_alarms()
    alarm_count = pending_alarms.count()

    # Prochains rendez-vous
    upcoming_appointments = Appointment.objects.filter(
        date_time__gte=timezone.now(),
        status='Scheduled',
    ).select_related('patient')[:10]

    context = {
        'total_patients_today': total_patients_today,
        'total_appointments_today': total_appointments_today,
        'total_appointments_week': total_appointments_week,
        'alarm_count': alarm_count,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'clinic/dashboard.html', context)


# ───────────────────────────────────────────
# 2. Gestion des patients
# ───────────────────────────────────────────

def patient_list(request):
    """List all patients with search."""
    query = request.GET.get('q', '')
    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone__icontains=query)
            | Q(cin__icontains=query)
        )

    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'clinic/patient_list.html', context)


def patient_create(request):
    """Create a new patient."""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Patient added successfully!'))
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'clinic/patient_form.html', {
        'form': form,
        'title': _('New Patient'),
    })


def patient_edit(request, pk):
    """Edit an existing patient."""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, _('Patient updated successfully!'))
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'clinic/patient_form.html', {
        'form': form,
        'title': _('Edit — %(name)s') % {'name': patient.full_name},
        'patient': patient,
    })


def patient_delete(request, pk):
    """Delete a patient."""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        patient.delete()
        messages.success(request, _('Patient deleted successfully!'))
        return redirect('patient_list')

    return render(request, 'clinic/patient_confirm_delete.html', {
        'patient': patient,
    })


# ───────────────────────────────────────────
# 3. Gestion des rendez-vous
# ───────────────────────────────────────────

def appointment_list(request):
    """Display today's and upcoming appointments."""
    today = timezone.localdate()

    today_appointments = Appointment.objects.filter(
        date_time__date=today,
    ).select_related('patient')

    upcoming_appointments = Appointment.objects.filter(
        date_time__date__gt=today,
        status='Scheduled',
    ).select_related('patient')[:15]

    context = {
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'clinic/appointment_list.html', context)


def appointment_create(request):
    """Create a new appointment."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment created successfully!'))
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'clinic/appointment_form.html', {
        'form': form,
        'title': _('New Appointment'),
    })


def appointment_edit(request, pk):
    """Edit an existing appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment updated successfully!'))
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'clinic/appointment_form.html', {
        'form': form,
        'title': _('Edit Appointment'),
        'appointment': appointment,
    })


def appointment_delete(request, pk):
    """Delete an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, _('Appointment deleted successfully!'))
        return redirect('appointment_list')

    return render(request, 'clinic/appointment_confirm_delete.html', {
        'appointment': appointment,
    })


# ───────────────────────────────────────────
# 4. Agenda hebdomadaire
# ───────────────────────────────────────────

def weekly_agenda(request):
    """Optimized weekly calendar view (next 7 days)."""
    today = timezone.localdate()
    end_date = today + timedelta(days=6)
    
    week_appointments = Appointment.objects.filter(
        date_time__date__gte=today,
        date_time__date__lte=end_date,
        status='Scheduled',
    ).select_related('patient').order_by('date_time')
    
    appointments_by_date = {}
    for rdv in week_appointments:
        rdv_date = timezone.localtime(rdv.date_time).date()
        if rdv_date not in appointments_by_date:
            appointments_by_date[rdv_date] = []
        appointments_by_date[rdv_date].append(rdv)

    days = []
    for i in range(7):
        current_day = today + timedelta(days=i)
        days.append({
            'date': current_day,
            'appointments': appointments_by_date.get(current_day, []),
        })

    return render(request, 'clinic/weekly_agenda.html', {'days': days})


# ───────────────────────────────────────────
# 5. Système d'alarmes
# ───────────────────────────────────────────

def alarm_list(request):
    """Display alarms (patients to contact)."""
    alarms = Appointment.objects.get_pending_alarms()

    return render(request, 'clinic/alarm_list.html', {
        'alarms': alarms,
    })


@require_POST
def mark_contacted(request, pk):
    """Mark an appointment as 'patient contacted'."""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        appointment.contacted_for_reminder = True
        appointment.save()
    messages.success(
        request,
        _('%(name)s has been marked as contacted.') % {
            'name': appointment.patient.full_name,
        },
    )

    return redirect('alarm_list')
