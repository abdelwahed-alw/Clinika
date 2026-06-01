# Clinika — Medical Clinic Management

![Clinika Banner](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white) ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)

Clinika is a modern, responsive Django application designed for the complete management of a medical clinic. It streamlines day-to-day operations by managing patient records, scheduling appointments, providing a weekly agenda view, and automating appointment reminders.

## ✨ Features

- **🧑‍⚕️ Patient Management** 
  - Add, edit, delete, and search patients (by name, CIN, or phone number).
  - Maintain comprehensive medical records including blood group, allergies, and chronic diseases.
  
- **📅 Appointment Scheduling**
  - Create, modify, and cancel appointments.
  - Classify appointments by type: *Consultation, Check-up, Control, Emergency, Follow-up*.
  - Strict double-booking prevention system.

- **📊 Smart Dashboard**
  - Get an at-a-glance overview of your clinic's statistics.
  - Track new patients today, today's appointments, and weekly appointment volume.

- **🗓️ Weekly Agenda**
  - An intuitive 7-day calendar view displaying all scheduled appointments for better time management.

- **🔔 Smart Reminder System (Alarms)**
  - Automatic detection of appointments within 48 hours that require a reminder call.
  - One-click "Mark as contacted" workflow to keep track of patient communications.

- **🌐 Bilingual Support (i18n)**
  - Full support for both **English** and **French**.
  - Seamless language switcher in the header to accommodate bilingual medical staff.

## 🛠️ Tech Stack

- **Backend:** Python 3.14, Django 6.0
- **Database:** SQLite (default)
- **Frontend:** HTML5, Tailwind CSS (via CDN)
- **Icons:** Font Awesome 6
- **Internationalization:** Django i18n (`gettext`)

## 🚀 Quick Start

1. **Clone the repository and enter the directory:**
   ```bash
   git clone <repo-url>
   cd Clinika
   ```

2. **Set up a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   Visit `http://localhost:8000` in your browser.

## 🧪 Development

### Generate Demo Data
Populate your database with sample patients and appointments to test the system:
```bash
python seed_data.py
```

### Run Tests
Execute the unit test suite to ensure business logic integrity (e.g., alarm logic and double-booking prevention):
```bash
python manage.py test
```

### Update Translations
If you add new translatable strings to the codebase, update the `.po` files and recompile them:
```bash
python manage.py makemessages -l fr
python manage.py compilemessages
```

## 📂 Project Structure

```text
Clinika/
├── cabinet_medical/        # Django project configuration (settings, urls, i18n, etc.)
├── clinic/                 # Main application module
│   ├── models.py           # Patient & Appointment models + Manager logic
│   ├── views.py            # CRUD operations, dashboard, agenda, alarms
│   ├── forms.py            # ModelForms for Patient & Appointment
│   ├── admin.py            # Django Admin interface configuration
│   ├── urls.py             # Route definitions for the clinic app
│   ├── tests.py            # Unit tests suite
│   └── templates/clinic/   # HTML templates styled with Tailwind CSS
├── locale/                 # Translation files (fr)
├── seed_data.py            # Script to generate sample demo data
└── manage.py               # Django management script
```
