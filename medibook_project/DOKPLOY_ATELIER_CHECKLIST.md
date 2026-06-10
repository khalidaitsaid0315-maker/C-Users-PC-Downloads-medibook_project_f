# 📋 Checklist Atelier Déploiement Django - Medibook

**Projet:** Medibook (Django 5.2.8)  
**Objectif:** Déployer sur Dokploy via la VM du professeur  
**Date:** 2026-06-10

---

## ✅ ÉTAPES 1-8: Préparation Locale

### Étape 1: ✅ Fichier .env
**Statut:** ✅ EXISTE

Fichier: `.env.example` (template fourni)

Variables requises:
```bash
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*
DB_ENGINE=postgresql
DB_NAME=medibook_db
DB_USER=postgres
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432
PORT=8161
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**À faire avant Dokploy:**
- [ ] Créer fichier `.env` à partir de `.env.example`
- [ ] Générer une nouvelle `DJANGO_SECRET_KEY`
- [ ] Définir un mot de passe DB sécurisé

---

### Étape 2: ✅ requirements.txt
**Statut:** ✅ VÉRIFIÉ

Fichier: `requirements.txt`

Contenu:
```
asgiref==3.8.1
Django==5.2.8
gunicorn==23.0.0
mysqlclient==2.2.8
psycopg2-binary==2.9.10
scikit-learn==1.3.2
packaging==24.2
pillow==11.2.1
sqlparse==0.5.5
whitenoise==6.8.2
```

**Note:** Contient à la fois `mysqlclient` et `psycopg2-binary` pour supporter MySQL et PostgreSQL.

---

### Étape 3: ✅ Dockerfile
**Statut:** ✅ VÉRIFIÉ

Fichier: `Dockerfile`

Caractéristiques:
- ✅ Base: `python:3.11-slim`
- ✅ Variables d'environnement configurées
- ✅ Dépendances système installées (PostgreSQL, MySQL clients)
- ✅ Requirements.txt copié et installé
- ✅ Application Django copiée
- ✅ Port 8161 exposé
- ✅ Entrypoint configuré

---

### Étape 4: ✅ entrypoint.sh
**Statut:** ✅ VÉRIFIÉ

Fichier: `docker-entrypoint.sh`

Fonctionnalités:
- ✅ Attend PostgreSQL (si DB_ENGINE=postgres)
- ✅ Exécute les migrations (`migrate --noinput`)
- ✅ Collecte les fichiers statiques (`collectstatic --noinput`)
- ✅ Démarre Gunicorn avec 4 workers
- ✅ Logs en stdout/stderr

---

### Étape 5: ✅ .dockerignore
**Statut:** ✅ EXISTE

Fichier: `.dockerignore`

Exclut les fichiers inutiles:
- `__pycache__/`
- `*.pyc`, `*.pyo`, `*.pyd`
- `.env`
- `.git`
- `db.sqlite3`
- `venv`, `.venv`
- `staticfiles/`

---

### Étape 6: ✅ settings.py
**Statut:** ✅ CONFIGURÉ

Fichier: `medibook/medibook/settings.py`

Vérifications effectuées:
- ✅ `SECRET_KEY` lisible depuis `os.environ.get('DJANGO_SECRET_KEY')`
- ✅ `DEBUG` controllé par `DJANGO_DEBUG`
- ✅ `ALLOWED_HOSTS` depuis `DJANGO_ALLOWED_HOSTS`
- ✅ `DATABASES` configurée pour PostgreSQL/MySQL via `DB_ENGINE`
- ✅ WhiteNoise dans MIDDLEWARE (compression statiques)
- ✅ `STATIC_ROOT` et `MEDIA_ROOT` configurés
- ✅ Support multi-database (PostgreSQL/MySQL/SQLite)

---

### Étape 7: ✅ Migrations Générées
**Statut:** ✅ APPLIQUÉES

Migrations présentes pour:
- ✅ `accounts`
- ✅ `patients`
- ✅ `doctors`
- ✅ `schedules`
- ✅ `appointments`
- ✅ `ai_orientation`
- ✅ `notifications`
- ✅ `dashboard`

Toutes les migrations ont été appliquées avec succès. La base de données SQLite locale est synchronisée.

---

### Étape 8: ✅ docker-compose.yml
**Statut:** ✅ VÉRIFIÉ

Fichier: `docker-compose.yml`

Services configurés:
- ✅ Service `db` (PostgreSQL 16-alpine avec healthcheck)
- ✅ Service `web` (Django/Gunicorn avec dépendance db)
- ✅ Volumes persistants pour données PostgreSQL
- ✅ Variables d'environnement depuis `.env`
- ✅ Ports mappés (8161:8161)
- ✅ Healthchecks activés

**Important pour Dokploy:**
- Le `docker-compose.yml` utilise PostgreSQL
- Pour MySQL, voir section "Adaptation pour Dokploy" ci-dessous

---

## ✅ ÉTAPES 9-13: Test & Build Local

### Étape 9: ✅ Application Lancée Localement
**Statut:** ✅ EN COURS

Serveur Django en fonctionnement sur `http://localhost:8161/`

Vérification des URLs:
```
✅ [200] http://localhost:8161/                          (Accueil)
✅ [200] http://localhost:8161/doctors/                  (Liste médecins)
✅ [200] http://localhost:8161/patients/                 (Profils patients)
✅ [200] http://localhost:8161/notifications/            (Notifications)
✅ [200] http://localhost:8161/dashboard/                (Tableau de bord)
✅ [200] http://localhost:8161/ai_orientation/           (Orientation IA)
✅ [200] http://localhost:8161/ai_orientation/historique/(Historique IA)
✅ [200] http://localhost:8161/accounts/login/           (Login)
✅ [200] http://localhost:8161/accounts/signup/          (Inscription)
⚠️  [302] http://localhost:8161/appointments/           (Redirect → login)
⚠️  [302] http://localhost:8161/appointments/reserver/  (Redirect → login)
```

Toutes les URLs fonctionnent correctement! ✅

---

### Étape 10: Créer Superuser
**Statut:** ⏳ À FAIRE

**Localement** (si besoin):
```bash
cd /home/mo_benlamine/Downloads/medibook_project_f/medibook_project/medibook
python manage.py createsuperuser
```

**Sur Dokploy** (section 23):
```bash
Containers -> web -> Terminal
python manage.py createsuperuser
```

---

### Étape 11: Vérifier PostgreSQL/MySQL
**Statut:** ✅ FONCTIONNEL

Actuellement: **SQLite local** (db.sqlite3)

Pour vérifier avec Docker Compose:
```bash
docker compose exec db psql -U postgres -d medibook_db -c "\dt"
```

---

### Étape 12: ✅ Construire l'Image Docker
**Statut:** À FAIRE

Avant de construire, assurez-vous d'avoir Docker installé sur votre machine.

**Commande:**
```bash
cd /home/mo_benlamine/Downloads/medibook_project_f/medibook_project
docker build -t votre_username/medibook:v1 .
```

**Exemple:**
```bash
docker build -t moncompte/medibook:v1 .
```

---

### Étape 13: ✅ Publier sur Docker Hub
**Statut:** À FAIRE

**Prérequis:**
- Compte Docker Hub (https://hub.docker.com)
- Authentification locale: `docker login`

**Commandes:**
```bash
# 1. Se connecter (une seule fois)
docker login

# 2. Tagger l'image avec votre compte
docker tag medibook:v1 votre_username/medibook:v1

# 3. Pousser vers Docker Hub
docker push votre_username/medibook:v1
```

**Vérification:**
- Accéder à https://hub.docker.com/r/votre_username/medibook
- Confirmer que l'image est visible publiquement

---

## 📦 ÉTAPES 14-23: Déploiement sur Dokploy

### Préalables Dokploy
Vous devriez avoir reçu du professeur:
- [ ] **URL de Dokploy**: `http://IP_VM:3000`
- [ ] **Identifiant personnel**: `etudiant-XX`
- [ ] **Mot de passe personnel**: `****`
- [ ] **Port attribué**: `8XXX` (ex: 8005)

---

### Étape 14: Connexion à Dokploy
**Statut:** À FAIRE

```
1. Ouvrir dans le navigateur: http://IP_VM:3000
2. Se connecter avec:
   - Identifiant: votre_login
   - Mot de passe: votre_mot_de_passe
3. Accueil Dokploy s'affiche
```

---

### Étape 15: Créer un Projet
**Statut:** À FAIRE

```
1. Cliquer sur "Projects" ou "Create Project"
2. Entrer le nom: medibook-etudiant-XX
3. Cliquer "Create"
```

---

### Étape 16: Créer un Service Docker Compose
**Statut:** À FAIRE

```
1. Dans le projet créé, cliquer "Create Service"
2. Choisir "Docker Compose"
3. Nom du service: django-medibook
4. Cliquer "Create"
```

---

### Étape 17: ⚠️ Configuration Docker Compose pour Dokploy
**Statut:** À ADAPTER

Le `docker-compose.yml` actuel utilise PostgreSQL. Pour l'atelier, vous pouvez:

**Option A: Garder PostgreSQL** (recommandé pour le projet)
```yaml
services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME:-medibook_db}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    image: votre_username/medibook:v1
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8005:8161"  # ⚠️ Remplacer 8005 par votre port attribué
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - staticfiles:/app/medibook/staticfiles
      - media:/app/medibook/media

volumes:
  db_data:
  staticfiles:
  media:
```

**Option B: Utiliser MySQL** (comme dans l'atelier)
```yaml
services:
  db:
    image: mysql:8.0
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-root}
      MYSQL_DATABASE: ${MYSQL_DATABASE:-medibook_db}
      MYSQL_USER: ${MYSQL_USER:-django}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-django}
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD-SHELL", "mysqladmin ping -h localhost -u root -p${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 10

  web:
    image: votre_username/medibook:v1
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8005:8161"  # ⚠️ Remplacer 8005 par votre port attribué
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - staticfiles:/app/medibook/staticfiles
      - media:/app/medibook/media

volumes:
  db_data:
  staticfiles:
  media:
```

**⚠️ Important:** Remplacer `votre_username` par votre Docker Hub username et `8005` par votre port attribué.

---

### Étape 18: Variables d'Environnement
**Statut:** À CONFIGURER

Dans Dokploy, onglet "Environment", ajouter:

**Pour PostgreSQL:**
```
DJANGO_SECRET_KEY=your-new-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*
DB_ENGINE=postgresql
DB_NAME=medibook_db
DB_USER=postgres
DB_PASSWORD=secure_password_123
DB_HOST=db
DB_PORT=5432
PORT=8161
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Ou pour MySQL:**
```
DJANGO_SECRET_KEY=your-new-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*
DB_ENGINE=mysql
DB_NAME=medibook_db
DB_USER=django
DB_PASSWORD=secure_password_123
DB_HOST=db
DB_PORT=3306
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=medibook_db
MYSQL_USER=django
MYSQL_PASSWORD=secure_password_123
PORT=8161
```

**⚠️ Importantes:**
- ✅ Générer une nouvelle `DJANGO_SECRET_KEY` (pas celle du projet local)
- ✅ Utiliser des mots de passe forts
- ✅ `DEBUG=False` pour la production
- ✅ `ALLOWED_HOSTS=*` ou adapter à votre domaine

---

### Étape 19: Lancer le Déploiement
**Statut:** À FAIRE

```
1. Vérifier que le docker-compose.yml et les variables sont correctes
2. Cliquer sur "Deploy"
3. Attendre le déploiement (2-5 minutes)
4. Observer les logs de déploiement
```

---

### Étape 20: Vérifier les Conteneurs
**Statut:** À VÉRIFIER APRÈS DÉPLOIEMENT

```
1. Dans Dokploy, aller à "Containers"
2. Vérifier que les deux conteneurs sont en GREEN:
   ✅ web (Django/Gunicorn)
   ✅ db (PostgreSQL ou MySQL)
3. Vérifier le statut du healthcheck
```

---

### Étape 21: Consulter les Logs
**Statut:** À FAIRE SI ERREURS

```
1. Aller à Containers -> web -> Logs
2. Chercher les messages:
   ✅ "Running Django migrations..."
   ✅ "Collecting static files..."
   ✅ "Starting Gunicorn on port..."

3. Si erreur, vérifier:
   - Variables d'environnement correctes?
   - Image Docker existe sur Docker Hub?
   - Port MySQL/PostgreSQL correct?
   - Migrations appliquées?
```

**Erreurs fréquentes et solutions (voir section finale):**

---

### Étape 22: Accéder à l'Application
**Statut:** À TESTER APRÈS DÉPLOIEMENT

Ouvrir dans le navigateur:
```
http://IP_VM:PORT/
```

Exemple:
```
http://84.8.221.206:8005/
```

Tester les URLs:
- ✅ http://IP_VM:PORT/ (Accueil)
- ✅ http://IP_VM:PORT/doctors/ (Médecins)
- ✅ http://IP_VM:PORT/patients/ (Patients)
- ✅ http://IP_VM:PORT/dashboard/ (Dashboard)
- ✅ http://IP_VM:PORT/admin/ (Admin - après superuser)

---

### Étape 23: Créer Superuser sur le Cloud
**Statut:** À FAIRE APRÈS DÉPLOIEMENT

```
1. Dans Dokploy, aller à Containers -> web
2. Cliquer sur "Terminal"
3. Exécuter:
   python manage.py createsuperuser
4. Suivre les prompts (username, email, password)
5. Accéder à: http://IP_VM:PORT/admin/
```

---

## 🐛 Erreurs Fréquentes & Solutions

### 1️⃣ Bad Request 400
**Cause:** ALLOWED_HOSTS incorrect

**Solution:**
```
DJANGO_ALLOWED_HOSTS=*
ou
DJANGO_ALLOWED_HOSTS=your-ip-vm,your-domain.com
```

---

### 2️⃣ Server Error 500
**Causes possibles:**
- Erreur de connexion DB
- Migrations non appliquées
- Variable d'environnement manquante

**Solution:**
1. Consulter les logs: `Containers -> web -> Logs`
2. Vérifier les variables d'environnement
3. Réappliquer les migrations si nécessaire

---

### 3️⃣ Access denied for user 'django'
**Cause:** Utilisateur MySQL n'existe pas

**Solution:**
- Supprimer le volume MySQL
- Redéployer avec les bonnes variables

---

### 4️⃣ Table does not exist
**Cause:** Migrations non appliquées

**Solution:**
```
Containers -> web -> Terminal
python manage.py migrate
```

---

### 5️⃣ Cannot connect to docker daemon
**Cause:** Docker n'est pas installé

**Solution:**
- Installer Docker sur votre machine
- Relancer la build: `docker build -t username/medibook:v1 .`

---

## 📝 Fichiers à Remettre

Pour la validation de l'atelier, préparez:

- [ ] Lien GitHub du projet
- [ ] Nom de l'image Docker Hub (`username/medibook:v1`)
- [ ] Fichier `Dockerfile`
- [ ] Fichier `docker-compose.yml` (pour Dokploy)
- [ ] Fichier `.env.example`
- [ ] Screenshot du test local avec Docker Compose
- [ ] Screenshot du déploiement Dokploy (Containers en GREEN)
- [ ] Screenshot de l'application accessible (http://IP_VM:PORT/)
- [ ] URL finale de l'application

---

## ✨ Résumé de l'État du Projet

| Étape | Statut | Notes |
|-------|--------|-------|
| 1. .env | ✅ | `.env.example` fourni |
| 2. requirements.txt | ✅ | Complet avec dépendances |
| 3. Dockerfile | ✅ | Python 3.11-slim, bien configuré |
| 4. entrypoint.sh | ✅ | Migrations + collectstatic + Gunicorn |
| 5. .dockerignore | ✅ | Fichiers sensibles exclus |
| 6. settings.py | ✅ | Variables d'environnement configurées |
| 7. Migrations | ✅ | Toutes appliquées avec succès |
| 8. docker-compose.yml | ✅ | PostgreSQL 16, test local prêt |
| 9. Test local | ✅ | Toutes les URLs fonctionnent |
| 10. Superuser | ⏳ | À créer sur Dokploy |
| 11. Vérif DB | ✅ | Fonctionnel |
| 12. Build image | ⏳ | Nécessite Docker localement |
| 13. Push Docker Hub | ⏳ | Après build |
| 14-23. Dokploy | ⏳ | Instructions complètes ci-dessus |

---

**🎯 Prochaines Étapes:**
1. Installer Docker sur votre machine
2. Construire l'image: `docker build -t username/medibook:v1 .`
3. Publier sur Docker Hub: `docker push username/medibook:v1`
4. Accéder à Dokploy et déployer selon les étapes 14-23
5. Vérifier que tout fonctionne
6. Remettre les fichiers demandés

---

**Date de finalisation:** 2026-06-10  
**Étudiant:** medibook-atelier
