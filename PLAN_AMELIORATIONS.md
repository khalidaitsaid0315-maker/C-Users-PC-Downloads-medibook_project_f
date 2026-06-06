# Plan d'Améliorations - MediBook Django

## 🚀 Actions Immédiates à Effectuer

### 1. TESTS UNITAIRES (Priorité: HAUTE)

**Fichier à créer**: `medibook/appointments/tests.py`
```python
from django.test import TestCase
from django.contrib.auth.models import User
from patients.models import ProfilPatient
from doctors.models import Medecin, Specialite
from appointments.models import RendezVous
from datetime import date, time

class RendezVousTestCase(TestCase):
    def setUp(self):
        self.specialite = Specialite.objects.create(name="Cardiologie")
        self.user_doc = User.objects.create_user(username="doctor", password="test123")
        self.medecin = Medecin.objects.create(
            user=self.user_doc,
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
            telephone_professionnel="0612345678",
            specialite=self.specialite,
            adresse_cabinet="123 Rue de Paris",
        )
        self.user_patient = User.objects.create_user(username="patient", password="test123")
        self.patient = ProfilPatient.objects.create(
            user=self.user_patient,
            nom="Martin",
            prenom="Pierre",
            email="pierre@example.com",
            telephone="0698765432",
            date_de_naissance="1990-01-01",
        )

    def test_rendezvous_creation(self):
        rdv = RendezVous.objects.create(
            patient=self.patient,
            medecin=self.medecin,
            specialite=self.specialite,
            date=date.today(),
            heure=time(10, 0),
            motif="Consultation",
        )
        self.assertEqual(rdv.statut, "en_attente")

    def test_unique_constraint_rendezvous(self):
        """Test qu'on ne peut pas avoir deux RDV au même créneau"""
        rdv1 = RendezVous.objects.create(
            patient=self.patient,
            medecin=self.medecin,
            specialite=self.specialite,
            date=date.today(),
            heure=time(10, 0),
            motif="Consultation",
        )
        # Créer un second RDV au même créneau devrait échouer
        with self.assertRaises(Exception):
            RendezVous.objects.create(
                patient=self.patient,
                medecin=self.medecin,
                specialite=self.specialite,
                date=date.today(),
                heure=time(10, 0),
                motif="Consultation",
            )
```

### 2. GROUPES DE RÔLES (Priorité: HAUTE)

**Fichier à créer**: `medibook/accounts/migrations/0002_add_groups.py`
```python
from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups(apps, schema_editor):
    patient_group, created = Group.objects.get_or_create(name='Patient')
    doctor_group, created = Group.objects.get_or_create(name='Doctor')
    admin_group, created = Group.objects.get_or_create(name='Admin')

    # Ajouter les permissions aux groupes
    # Pour Patient: voir ses RDV, les modifier, les annuler
    # Pour Doctor: voir ses RDV, confirmer/annuler
    # Pour Admin: voir tout, gérer les utilisateurs

def reverse_groups(apps, schema_editor):
    Group.objects.filter(name__in=['Patient', 'Doctor', 'Admin']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_groups, reverse_groups),
    ]
```

**Modifier**: `medibook/accounts/decorators.py`
```python
from django.core.exceptions import PermissionDenied
from functools import wraps

def require_group(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.groups.filter(name=group_name).exists():
                raise PermissionDenied(f"Vous devez être un {group_name} pour accéder à cette page.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### 3. AMÉLIORATION CI/CD (Priorité: HAUTE)

**Fichier à modifier**: `.github/workflows/ci-cd.yml`
```yaml
name: MediBook CI/CD

on:
  push:
    branches: ["main", "master"]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: medibook_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install flake8 coverage safety

      - name: Security check with safety
        run: safety check --json

      - name: Code quality check with flake8
        run: flake8 medibook --count --select=E9,F63,F7,F82 --show-source --statistics

      - name: Run migrations check
        working-directory: medibook
        env:
          DB_ENGINE: postgres
          DB_NAME: medibook_test
          DB_USER: postgres
          DB_PASSWORD: postgres
          DB_HOST: localhost
          DB_PORT: 5432
        run: python manage.py makemigrations --check --dry-run

      - name: Run Django checks
        working-directory: medibook
        run: python manage.py check

      - name: Run unit tests with coverage
        working-directory: medibook
        env:
          DB_ENGINE: postgres
          DB_NAME: medibook_test
          DB_USER: postgres
          DB_PASSWORD: postgres
          DB_HOST: localhost
          DB_PORT: 5432
        run: coverage run --source='.' manage.py test

      - name: Generate coverage report
        working-directory: medibook
        run: coverage report -m

      - name: Build Docker image
        run: docker build . -t medibook:${{ github.sha }}

      - name: Scan Docker image with trivy (optional)
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: medibook:${{ github.sha }}
          format: 'sarif'

      - name: Login to Docker Hub
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Push to Docker Hub
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: docker push medibook:${{ github.sha }}

      - name: Notify on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Build failed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 4. README.md (Priorité: HAUTE)

**Fichier à créer**: `README.md`
```markdown
# 🏥 MediBook - Plateforme de Gestion de Rendez-vous Médicaux

## 📋 Description

MediBook est une plateforme web moderne développée avec **Django** permettant la gestion complète des rendez-vous médicaux. Elle offre une expérience fluide aux patients, aux médecins et aux administrateurs.

### Caractéristiques principales:
- ✅ Recherche et filtrage de médecins par spécialité
- ✅ Réservation, modification et annulation de rendez-vous
- ✅ Gestion des disponibilités des médecins
- ✅ Système d'authentification sécurisé
- ✅ **Fonctionnalité IA** d'orientation vers une spécialité
- ✅ Tableaux de bord pour patients, médecins et administrateurs
- ✅ Notifications et rappels
- ✅ Déploiement containerisé avec Docker

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.13+
- Docker & Docker Compose
- PostgreSQL (ou SQLite pour développement)

### Option 1: Avec Docker Compose (Recommandé)

```bash
# Cloner le repository
git clone <url-du-repo>
cd medibook_project

# Copier le fichier .env
cp .env.example .env

# Démarrer les services
docker-compose up -d

# Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser

# Visiter http://localhost:8000
```

### Option 2: Installation Locale

```bash
# Créer un virtualenv
python -m venv venv
source venv/bin/activate  # Unix/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configuration
cd medibook
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver
```

---

## 📐 Architecture

### Structure du Projet
```
medibook_project/
├── medibook/                 # Dossier principal Django
│   ├── accounts/            # Gestion des utilisateurs
│   ├── patients/            # Profils patients
│   ├── doctors/             # Médecins et spécialités
│   ├── appointments/        # Rendez-vous
│   ├── schedules/           # Disponibilités
│   ├── dashboard/           # Tableaux de bord
│   ├── ai_orientation/      # Fonctionnalité IA
│   ├── notifications/       # Notifications
│   ├── templates/           # Templates HTML
│   ├── static/              # Fichiers statiques
│   ├── manage.py
│   └── medibook/            # Configuration Django
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

### Modèle de Données
```
┌─────────────┐      ┌──────────────┐
│   User      │      │ ProfilPatient│
│ (Django)    │◄─────┤              │
└─────────────┘      └──────────────┘

┌──────────────┐
│   Medecin    │
│              │
└──────────────┘
       ▲
       │
    ┌──┴───┐
    │      │
┌───┴──┐  ┌┴────────┐
│Specia│ │Disponib.│
│lité  │ │         │
└──────┘ └──────────┘
       │
       │
┌──────▼──────┐
│  RendezVous │
│             │
└──────────────┘
```

---

## 🎯 Fonctionnalités Détaillées

### 1. Gestion des Utilisateurs
- Inscription sécurisée des patients
- Connexion/déconnexion
- Profils utilisateur modifiables
- Récupération de mot de passe

### 2. Recherche et Filtrage
- Recherche de médecins par nom, email, spécialité
- Filtrage par spécialité
- Liste des spécialités disponibles

### 3. Réservation de Rendez-vous
- Sélection de médecin
- Choix du créneau disponible
- Précision du motif de consultation
- Confirmation automatique

### 4. Gestion des Rendez-vous
- Statuts: En attente, Confirmé, Annulé, Terminé, Absent
- Modification possible avant la date
- Annulation avec notification
- Historique complet

### 5. Intelligence Artificielle
Système d'orientation intelligent basé sur:
- **TF-IDF** pour l'analyse textuelle
- **Similarité cosinus** pour la comparaison
- **Mots-clés** pour la détection simple
- **Score de confiance** calculé automatiquement

Exemple:
```
Entrée: "Douleurs thoraciques et palpitations"
Recommandation: Cardiologie (Confiance: 85%)
```

### 6. Tableaux de Bord
- **Patient**: Prochains RDV, historique, statistiques
- **Médecin**: RDV du jour/semaine, confirmations, planning
- **Admin**: Statistiques globales, gestion des utilisateurs

---

## 🔒 Sécurité

### Fonctionnalités de Sécurité
- ✅ Protection CSRF sur tous les formulaires
- ✅ Validation des données côté serveur
- ✅ Authentification requise pour les opérations sensibles
- ✅ Hachage des mots de passe (PBKDF2)
- ✅ Gestion des variables sensibles via .env
- ✅ DEBUG désactivé en production

### Bonnes Pratiques Appliquées
- Chaque patient ne voit que ses propres RDV
- Chaque médecin ne voit que ses propres RDV
- Contraintes d'intégrité dans la base de données
- Validations métier dans les modèles

---

## 🐳 Déploiement

### Avec Docker Compose (Développement & Production locale)
```bash
docker-compose up -d
```

Services:
- **web** (Django): http://localhost:8000
- **db** (PostgreSQL): localhost:5432

### Variables d'Environnement (.env)
```env
DEBUG=False                          # True en dev, False en prod
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1   # Ajouter votre domaine en prod
DB_ENGINE=postgres                  # ou mysql, sqlite
DB_NAME=medibook_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db                          # ou localhost en local
DB_PORT=5432
TIME_ZONE=Africa/Casablanca
```

### Pour la Production
```bash
# Collecte des fichiers statiques
python manage.py collectstatic --noinput

# Migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Gunicorn
gunicorn medibook.wsgi:application --bind 0.0.0.0:8000
```

---

## 🧪 Tests

### Exécuter les tests
```bash
cd medibook
python manage.py test

# Avec couverture
coverage run --source='.' manage.py test
coverage report
```

### Tests disponibles
- Tests des modèles
- Tests des vues
- Tests des validations
- Tests d'authentification

---

## 📊 CI/CD Pipeline

Le projet utilise **GitHub Actions** pour:
- ✅ Tests automatiques
- ✅ Vérification de la qualité du code
- ✅ Scan de sécurité
- ✅ Construction Docker
- ✅ Publication sur Docker Hub (en cas de succès)

Fichier: `.github/workflows/ci-cd.yml`

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche: `git checkout -b feature/ma-feature`
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/ma-feature`
5. Créer une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT.

---

## 👥 Auteurs

- Développement: [Votre nom]
- Supervision: [Superviseur]

---

## 📞 Support

Pour les questions ou problèmes:
- Ouvrir une issue GitHub
- Consulter la documentation
- Contacter l'équipe de développement

---

## 🗺️ Roadmap

- [ ] Tests complets (100% coverage)
- [ ] API REST avec Django REST Framework
- [ ] Interface mobile responsive
- [ ] Notifications par email/SMS
- [ ] Intégration de paiement
- [ ] Graphiques et statistiques avancées
- [ ] Export en PDF

---

**Dernière mise à jour**: Juin 2026
```

### 5. MODÈLE AVIS (Priorité: MOYENNE)

**Ajouter au fichier** `medibook/appointments/models.py`:
```python
class Avis(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    rendezvous = models.OneToOneField(RendezVous, on_delete=models.CASCADE, related_name='avis')
    note = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Avis {self.note}/5 pour RDV #{self.rendezvous.id}"
```

### 6. AMÉLIORATION DU TABLEAU DE BORD PATIENT (Priorité: MOYENNE)

**Modifier** `medibook/dashboard/views.py`:
```python
@login_required
def patient_dashboard(request):
    patient = ProfilPatient.objects.get(user=request.user)
    today = date.today()
    
    prochains_rdv = patient.rendez_vous.filter(
        date__gte=today,
        statut__in=['en_attente', 'confirme']
    ).order_by('date', 'heure')
    
    rdv_passes = patient.rendez_vous.filter(
        date__lt=today,
        statut__in=['termine', 'absent']
    ).order_by('-date', '-heure')
    
    rdv_annules = patient.rendez_vous.filter(
        statut='annule'
    ).order_by('-date_creation')
    
    context = {
        'patient': patient,
        'prochains_rdv': prochains_rdv[:5],
        'rdv_passes': rdv_passes[:5],
        'rdv_annules': rdv_annules[:5],
    }
    return render(request, 'dashboard/patient_dashboard.html', context)
```

### 7. AJOUTER DES DIAGRAMMES (Priorité: BASSE)

**Créer** `docs/ARCHITECTURE.md`:
- Diagramme de cas d'utilisation (UML)
- Diagramme de classes (UML)
- Diagramme de flux des rendez-vous
- Architecture technique

---

## 📋 Checklist de Vérification

Avant la livraison finale:

### Tests & Qualité
- [ ] Tests unitaires écrits et passants
- [ ] Coverage > 80%
- [ ] Code lint check (flake8)
- [ ] Pas d'erreurs Django checks

### Documentation
- [ ] README.md complet
- [ ] Docstrings dans le code
- [ ] Diagrammes UML
- [ ] Guide d'installation

### Sécurité
- [ ] DEBUG=False en production
- [ ] SECRET_KEY unique et sécurisé
- [ ] CSRF protection validée
- [ ] Authentification testée
- [ ] Permissions testées

### Déploiement
- [ ] Docker build sans erreurs
- [ ] Docker-compose up sans erreurs
- [ ] Migrations automatiques testées
- [ ] Variables .env configurées

### Fonctionnalités
- [ ] Tous les CRUD des rendez-vous
- [ ] Fonctionnalité IA testée
- [ ] Notifications générées
- [ ] Tableaux de bord affichent les données

---

## 🎓 Ressources

- [Documentation Django](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [scikit-learn Guide](https://scikit-learn.org/)
- [GitHub Actions](https://github.com/features/actions)

---

**Généré le**: 2 Juin 2026
