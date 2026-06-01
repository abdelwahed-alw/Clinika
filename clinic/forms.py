from django import forms
from .models import Patient, Appointment


class PatientForm(forms.ModelForm):
    """Formulaire de création/modification d'un patient."""

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
                'placeholder': 'Prénom du patient',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
                'placeholder': 'Nom du patient',
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
                'placeholder': 'Numéro CIN',
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
                'placeholder': 'Adresse complète',
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
                'placeholder': 'Ville',
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
                'placeholder': 'Liste des allergies connues...',
            }),
            'chronic_diseases': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white resize-none',
                'placeholder': 'Liste des maladies chroniques...',
            }),
        }


class AppointmentForm(forms.ModelForm):
    """Formulaire de création/modification d'un rendez-vous."""

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
                'placeholder': 'Motif du rendez-vous...',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
                         'focus:border-teal-500 focus:ring-2 focus:ring-teal-200 '
                         'transition-all duration-200 bg-white',
            }),
        }
