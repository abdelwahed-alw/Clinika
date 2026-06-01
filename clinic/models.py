from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Patient(models.Model):
    """Modèle représentant un patient du cabinet médical."""

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

    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    date_of_birth = models.DateField("Date de naissance")
    cin = models.CharField("CIN", max_length=20, blank=True, null=True)
    phone = models.CharField("Téléphone", max_length=20)
    email = models.EmailField("Email", blank=True, null=True)
    address = models.TextField("Adresse", blank=True, null=True)
    city = models.CharField("Ville", max_length=100, blank=True, null=True)
    blood_group = models.CharField(
        "Groupe sanguin",
        max_length=5,
        choices=BLOOD_GROUP_CHOICES,
        blank=True,
        null=True,
    )
    allergies = models.TextField("Allergies", blank=True)
    chronic_diseases = models.TextField("Maladies chroniques", blank=True)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)

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
        """Calculer l'âge du patient à partir de sa date de naissance."""
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
        """Récupérer les rendez-vous nécessitant un rappel (≤ 2 jours, futur strict, non contacté)."""
        now = timezone.now()
        limit_date = timezone.localdate() + timezone.timedelta(days=2)
        
        return self.filter(
            date_time__gte=now,
            date_time__date__lte=limit_date,
            contacted_for_reminder=False,
            status='Planifié',
        ).select_related('patient')


class Appointment(models.Model):
    """Modèle représentant un rendez-vous médical."""

    TYPE_CHOICES = [
        ('Consultation', 'Consultation'),
        ('Bilan', 'Bilan'),
        ('Contrôle', 'Contrôle'),
        ('Urgence', 'Urgence'),
        ('Suivi', 'Suivi'),
    ]

    STATUS_CHOICES = [
        ('Planifié', 'Planifié'),
        ('Annulé', 'Annulé'),
        ('Terminé', 'Terminé'),
    ]

    objects = AppointmentManager()

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Patient",
    )
    date_time = models.DateTimeField("Date et heure")
    type = models.CharField(
        "Type de rendez-vous",
        max_length=20,
        choices=TYPE_CHOICES,
        default='Consultation',
    )
    reason = models.TextField("Motif")
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default='Planifié',
    )
    contacted_for_reminder = models.BooleanField(
        "Contacté pour rappel",
        default=False,
    )

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
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
                    'date_time': "Un rendez-vous est déjà planifié à cette date et heure exactes."
                })

    def __str__(self):
        local_dt = timezone.localtime(self.date_time)
        return (
            f"RDV - {self.patient.full_name} "
            f"le {local_dt.strftime('%d/%m/%Y à %H:%M')}"
        )
