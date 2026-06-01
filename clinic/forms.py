from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Patient, Appointment


class PatientForm(forms.ModelForm):
    """Form for creating/editing a patient."""

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'cin',
            'phone', 'email', 'address', 'city',
            'blood_group', 'allergies', 'chronic_diseases',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
                'placeholder': _('Patient first name'),
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
                'placeholder': _('Patient last name'),
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
            }),
            'cin': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
                'placeholder': _('CIN number'),
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
                'placeholder': '06XXXXXXXX',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
                'placeholder': 'email@example.com',
            }),
            'address': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white resize-none',
                'placeholder': _('Full address'),
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
                'placeholder': _('City'),
            }),
            'blood_group': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
            }),
            'allergies': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white resize-none',
                'placeholder': _('List of known allergies...'),
            }),
            'chronic_diseases': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white resize-none',
                'placeholder': _('List of chronic diseases...'),
            }),
        }


class AppointmentForm(forms.ModelForm):
    """Form for creating/editing an appointment."""

    class Meta:
        model = Appointment
        fields = ['patient', 'date_time', 'type', 'reason', 'status']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
            }),
            'date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
            }),
            'type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
            }),
            'reason': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white resize-none',
                'placeholder': _('Reason for appointment...'),
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
            }),
        }
