# Medical Clinic Management

Django application for managing a medical clinic — patients, appointments, weekly agenda, and automatic reminders.

## Features

- **Patient Management** — Add, edit, delete and search (name, CIN, phone). Complete medical record: blood group, allergies, chronic diseases.
- **Appointment Scheduling** — Create, modify and cancel with classification (Consultation, Check-up, Control, Emergency, Follow-up). Double-booking prevention.
- **Dashboard** — At-a-glance statistics: new patients today, today's/week's appointments, pending reminders.
- **Weekly Agenda** — 7-day calendar view with all scheduled appointments.
- **Smart Reminder System** — Automatic detection of appointments within 48h without follow-up, with one-click "Mark as contacted" action.

## Tech Stack

- Python 3.14 / Django 6.0
- SQLite
- Tailwind CSS (CDN)
- Font Awesome 6

## Quick Start

```bash
git clone <repo-url>
cd <project-directory>
python -m venv venv && source venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

### Demo Data

```bash
python seed_data.py
```

### Run Tests

```bash
python manage.py test
```

## Project Structure

```
cabinet_medical/            # Django configuration (settings, urls, wsgi, asgi)
clinic/                     # Main application
├── models.py               # Patient & Appointment models
├── views.py                # CRUD views, dashboard, agenda, alarms
├── forms.py                # ModelForms for Patient & Appointment
├── admin.py                # Admin interface configuration
├── urls.py                 # Route definitions
├── tests.py                # Unit tests
└── templates/clinic/       # HTML templates (Tailwind CSS)
seed_data.py                # Demo data generation script
```
