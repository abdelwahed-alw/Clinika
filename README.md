# Gestion Cabinet Médical

Application Django de gestion d'un cabinet médical — patients, rendez-vous, agenda hebdomadaire et rappels automatiques.

## Fonctionnalités

- **Gestion des patients** — Ajout, modification, suppression et recherche (nom, CIN, téléphone). Fiche médicale complète : groupe sanguin, allergies, maladies chroniques.
- **Planification des rendez-vous** — Création, modification et annulation avec classification (Consultation, Bilan, Contrôle, Urgence, Suivi). Prévention des doubles réservations.
- **Tableau de bord** — Statistiques en un coup d'œil : nouveaux patients du jour, rendez-vous du jour/de la semaine, rappels en attente.
- **Agenda hebdomadaire** — Vue calendrier sur 7 jours avec l'ensemble des rendez-vous planifiés.
- **Système de rappels intelligent** — Détection automatique des rendez-vous dans les 48h sans relance, avec action "Marquer comme contacté" en un clic.

## Stack technique

- Python 3.14 / Django 6.0
- SQLite
- Tailwind CSS (CDN)
- Font Awesome 6

## Démarrage rapide

```bash
git clone <repo-url>
cd <project-directory>
python -m venv venv && source venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

### Données de démonstration

```bash
python seed_data.py
```

### Lancer les tests

```bash
python manage.py test
```

## Structure du projet

```
cabinet_medical/            # Configuration Django (settings, urls, wsgi, asgi)
clinic/                     # Application principale
├── models.py               # Modèles Patient & Appointment
├── views.py                # Vues CRUD, dashboard, agenda, alarmes
├── forms.py                # ModelForms pour Patient & Appointment
├── admin.py                # Configuration de l'interface d'administration
├── urls.py                 # Définition des routes
├── tests.py                # Tests unitaires
└── templates/clinic/       # Templates HTML (Tailwind CSS)
seed_data.py                # Script de génération de données fictives
```
