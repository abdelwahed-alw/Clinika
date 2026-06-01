from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from .models import Patient, Appointment

class AlarmLogicTest(TestCase):
    def setUp(self):
        # Création d'un patient de test
        self.patient = Patient.objects.create(
            first_name="Test",
            last_name="Patient",
            date_of_birth="1990-01-01",
            phone="0600000000"
        )
        
        self.now = timezone.now()
        self.localdate = timezone.localdate()

    def test_get_pending_alarms(self):
        """
        Prouver mathématiquement que la logique d'alarme (≤ 2 jours) 
        filtre exactement les bons rendez-vous.
        """
        
        # 1. RDV Aujourd'hui (dans 2 heures) -> DOIT être dans l'alarme
        rdv_today = Appointment.objects.create(
            patient=self.patient,
            date_time=self.now + timedelta(hours=2),
            type="Consultation",
            reason="Aujourd'hui",
            status="Planifié",
            contacted_for_reminder=False
        )

        # 2. RDV dans exactement 2 jours -> DOIT être dans l'alarme
        rdv_2_days = Appointment.objects.create(
            patient=self.patient,
            date_time=self.now + timedelta(days=2),
            type="Consultation",
            reason="Dans 2 jours",
            status="Planifié",
            contacted_for_reminder=False
        )

        # 3. RDV dans 5 jours -> NE DOIT PAS être dans l'alarme (hors limite)
        rdv_5_days = Appointment.objects.create(
            patient=self.patient,
            date_time=self.now + timedelta(days=5),
            type="Consultation",
            reason="Dans 5 jours",
            status="Planifié",
            contacted_for_reminder=False
        )
        
        # 4. RDV passé (hier) -> NE DOIT PAS être dans l'alarme
        rdv_past = Appointment.objects.create(
            patient=self.patient,
            date_time=self.now - timedelta(days=1),
            type="Consultation",
            reason="Passé",
            status="Planifié",
            contacted_for_reminder=False
        )

        # 5. RDV dans 1 jour mais déjà contacté -> NE DOIT PAS être dans l'alarme
        rdv_contacted = Appointment.objects.create(
            patient=self.patient,
            date_time=self.now + timedelta(days=1),
            type="Consultation",
            reason="Déjà contacté",
            status="Planifié",
            contacted_for_reminder=True
        )

        # Récupération des alarmes via le Manager
        alarms = Appointment.objects.get_pending_alarms()

        # Assertions
        self.assertEqual(alarms.count(), 2)
        self.assertIn(rdv_today, alarms)
        self.assertIn(rdv_2_days, alarms)
        self.assertNotIn(rdv_5_days, alarms)
        self.assertNotIn(rdv_past, alarms)
        self.assertNotIn(rdv_contacted, alarms)

    def test_prevent_double_booking(self):
        """Test que la validation de modèle empêche les doubles rendez-vous."""
        dt = self.now + timedelta(days=1)
        
        # Créer le premier RDV
        Appointment.objects.create(
            patient=self.patient,
            date_time=dt,
            type="Consultation",
            reason="Premier RDV"
        )
        
        # Tenter d'en créer un deuxième à la même heure
        rdv_double = Appointment(
            patient=self.patient,
            date_time=dt,
            type="Bilan",
            reason="Double RDV"
        )
        
        from django.core.exceptions import ValidationError
        with self.assertRaisesMessage(ValidationError, "Un rendez-vous est déjà planifié à cette date et heure exactes."):
            rdv_double.clean()
