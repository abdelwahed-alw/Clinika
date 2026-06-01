"""
Data migration to convert French status/type values to English.

The original schema used French choice values (e.g. Planifié, Bilan).
The models have since been updated to use English values.
This migration converts existing data to match.
"""

from django.db import migrations


def convert_french_to_english(apps, schema_editor):
    Appointment = apps.get_model('clinic', 'Appointment')

    # Convert status values
    status_map = {
        'Planifié': 'Scheduled',
        'Annulé': 'Cancelled',
        'Terminé': 'Completed',
    }
    for french, english in status_map.items():
        Appointment.objects.filter(status=french).update(status=english)

    # Convert type values
    type_map = {
        'Bilan': 'Check-up',
        'Contrôle': 'Control',
        'Urgence': 'Emergency',
        'Suivi': 'Follow-up',
        # 'Consultation' stays the same in both languages
    }
    for french, english in type_map.items():
        Appointment.objects.filter(type=french).update(type=english)


def convert_english_to_french(apps, schema_editor):
    Appointment = apps.get_model('clinic', 'Appointment')

    status_map = {
        'Scheduled': 'Planifié',
        'Cancelled': 'Annulé',
        'Completed': 'Terminé',
    }
    for english, french in status_map.items():
        Appointment.objects.filter(status=english).update(status=french)

    type_map = {
        'Check-up': 'Bilan',
        'Control': 'Contrôle',
        'Emergency': 'Urgence',
        'Follow-up': 'Suivi',
    }
    for english, french in type_map.items():
        Appointment.objects.filter(type=english).update(type=french)


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_alter_appointment_options_and_more'),
    ]

    operations = [
        migrations.RunPython(
            convert_french_to_english,
            convert_english_to_french,
        ),
    ]
