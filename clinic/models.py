from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Patient(models.Model):
    """Model representing a patient in the medical practice."""

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    first_name = models.CharField("First name", max_length=100)
    last_name = models.CharField("Last name", max_length=100)
    date_of_birth = models.DateField("Date of birth")
    cin = models.CharField("CIN", max_length=20, blank=True, null=True)
    phone = models.CharField("Phone", max_length=20)
    email = models.EmailField("Email", blank=True, null=True)
    address = models.TextField("Address", blank=True, null=True)
    city = models.CharField("City", max_length=100, blank=True, null=True)
    blood_group = models.CharField(
        "Blood group",
        max_length=5,
        choices=BLOOD_GROUP_CHOICES,
        blank=True,
        null=True,
    )
    allergies = models.TextField("Allergies", blank=True)
    chronic_diseases = models.TextField("Chronic diseases", blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def age(self):
        """Calculate the patient's age from their date of birth."""
        today = timezone.localdate()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

class AppointmentManager(models.Manager):
    def get_pending_alarms(self):
        """Get appointments requiring a reminder (≤ 2 days, strictly future, not contacted)."""
        now = timezone.now()
        limit_date = timezone.localdate() + timezone.timedelta(days=2)
        
        return self.filter(
            date_time__gte=now,
            date_time__date__lte=limit_date,
            contacted_for_reminder=False,
            status='Scheduled',
        ).select_related('patient')


class Appointment(models.Model):
    """Model representing a medical appointment."""

    TYPE_CHOICES = [
        ('Consultation', 'Consultation'),
        ('Check-up', 'Check-up'),
        ('Control', 'Control'),
        ('Emergency', 'Emergency'),
        ('Follow-up', 'Follow-up'),
    ]

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    objects = AppointmentManager()

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Patient",
    )
    date_time = models.DateTimeField("Date and time")
    type = models.CharField(
        "Appointment type",
        max_length=20,
        choices=TYPE_CHOICES,
        default='Consultation',
    )
    reason = models.TextField("Reason")
    status = models.CharField(
        "Status",
        max_length=20,
        choices=STATUS_CHOICES,
        default='Scheduled',
    )
    contacted_for_reminder = models.BooleanField(
        "Contacted for reminder",
        default=False,
    )

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['date_time']

    def clean(self):
        super().clean()
        # Prevent double booking
        if self.date_time:
            overlapping = Appointment.objects.filter(
                date_time=self.date_time
            ).exclude(pk=self.pk)
            
            if overlapping.exists():
                raise ValidationError({
                    'date_time': "An appointment is already scheduled at this exact date and time."
                })

    def __str__(self):
        local_dt = timezone.localtime(self.date_time)
        return (
            f"Appt - {self.patient.full_name} "
            f"on {local_dt.strftime('%d/%m/%Y at %H:%M')}"
        )
