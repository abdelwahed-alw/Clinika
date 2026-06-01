"""
Script de peuplement de la base de données avec des données de test.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cabinet_medical.settings')
django.setup()

from datetime import timedelta
from django.utils import timezone
from clinic.models import Patient, Appointment


def seed():
    """Créer des données de test."""

    # Patients
    patients_data = [
        {
            'first_name': 'Fatima', 'last_name': 'Benali',
            'date_of_birth': '1985-03-15', 'cin': 'AB123456',
            'phone': '0661234567', 'email': 'fatima.benali@email.com',
            'city': 'Casablanca', 'blood_group': 'A+',
            'allergies': 'Pénicilline', 'chronic_diseases': '',
        },
        {
            'first_name': 'Ahmed', 'last_name': 'El Mansouri',
            'date_of_birth': '1990-07-22', 'cin': 'CD789012',
            'phone': '0677889900', 'email': 'ahmed.mansouri@email.com',
            'city': 'Rabat', 'blood_group': 'O+',
            'allergies': '', 'chronic_diseases': 'Diabète type 2',
        },
        {
            'first_name': 'Khadija', 'last_name': 'Ouazzani',
            'date_of_birth': '1978-11-08', 'cin': 'EF345678',
            'phone': '0655443322', 'email': '',
            'city': 'Fès', 'blood_group': 'B+',
            'allergies': 'Aspirine, Latex', 'chronic_diseases': 'Hypertension',
        },
        {
            'first_name': 'Youssef', 'last_name': 'Amrani',
            'date_of_birth': '1995-01-30', 'cin': 'GH901234',
            'phone': '0699887766',
            'city': 'Marrakech', 'blood_group': 'AB+',
            'allergies': '', 'chronic_diseases': '',
        },
        {
            'first_name': 'Sara', 'last_name': 'Tazi',
            'date_of_birth': '2000-06-12', 'cin': 'IJ567890',
            'phone': '0622334455', 'email': 'sara.tazi@email.com',
            'city': 'Tanger', 'blood_group': 'O-',
            'allergies': 'Sulfamides', 'chronic_diseases': 'Asthme',
        },
        {
            'first_name': 'Mohammed', 'last_name': 'Alaoui',
            'date_of_birth': '1970-09-25', 'cin': 'KL112233',
            'phone': '0644556677',
            'city': 'Casablanca', 'blood_group': 'A-',
            'allergies': '', 'chronic_diseases': 'Cholestérol',
        },
    ]

    patients = []
    for data in patients_data:
        p, created = Patient.objects.get_or_create(
            cin=data.get('cin', ''),
            defaults=data,
        )
        patients.append(p)
        status = "✓ Créé" if created else "→ Existe déjà"
        print(f"  {status}: {p.full_name}")

    # Appointments
    now = timezone.now()
    appointments_data = [
        # Aujourd'hui
        {
            'patient': patients[0],
            'date_time': now.replace(hour=9, minute=0),
            'type': 'Consultation', 'reason': 'Douleurs abdominales récurrentes',
            'status': 'Planifié',
        },
        {
            'patient': patients[1],
            'date_time': now.replace(hour=10, minute=30),
            'type': 'Contrôle', 'reason': 'Suivi glycémie trimestriel',
            'status': 'Planifié',
        },
        {
            'patient': patients[4],
            'date_time': now.replace(hour=14, minute=0),
            'type': 'Bilan', 'reason': 'Bilan annuel + spirométrie',
            'status': 'Planifié',
        },
        # Demain (alarme !)
        {
            'patient': patients[2],
            'date_time': now + timedelta(days=1, hours=2),
            'type': 'Consultation', 'reason': 'Contrôle tension artérielle',
            'status': 'Planifié', 'contacted_for_reminder': False,
        },
        {
            'patient': patients[3],
            'date_time': now + timedelta(days=1, hours=4),
            'type': 'Bilan', 'reason': 'Bilan sanguin complet',
            'status': 'Planifié', 'contacted_for_reminder': False,
        },
        # Dans 2 jours (alarme !)
        {
            'patient': patients[5],
            'date_time': now + timedelta(days=2, hours=1),
            'type': 'Suivi', 'reason': 'Suivi traitement cholestérol',
            'status': 'Planifié', 'contacted_for_reminder': False,
        },
        # Dans 3 jours
        {
            'patient': patients[0],
            'date_time': now + timedelta(days=3),
            'type': 'Contrôle', 'reason': 'Résultats analyses sanguines',
            'status': 'Planifié',
        },
        # Dans 5 jours
        {
            'patient': patients[4],
            'date_time': now + timedelta(days=5),
            'type': 'Consultation', 'reason': 'Renouvellement ordonnance',
            'status': 'Planifié',
        },
    ]

    print("\nRendez-vous:")
    for data in appointments_data:
        rdv, created = Appointment.objects.get_or_create(
            patient=data['patient'],
            date_time=data['date_time'],
            defaults=data,
        )
        status = "✓ Créé" if created else "→ Existe déjà"
        print(f"  {status}: {rdv}")

    print("\n✅ Données de test chargées avec succès !")


if __name__ == '__main__':
    print("Peuplement de la base de données...\n")
    print("Patients:")
    seed()
