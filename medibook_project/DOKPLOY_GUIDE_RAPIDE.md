# 🚀 Guide Rapide: Déploiement Medibook sur Dokploy

**Objectif:** Déployer l'application Medibook Django sur une machine virtuelle Cloud via Dokploy en 5 étapes.

---

## 📋 Informations à Recevoir du Professeur

Avant de commencer, assurez-vous d'avoir les informations suivantes :

| Élément | Valeur | Exemple |
|---------|--------|---------|
| **URL Dokploy** | http://IP_VM:3000 | http://192.168.1.100:3000 |
| **Identifiant** | etudiant-XX | etudiant-05 |
| **Mot de passe** | ****** | [fourni] |
| **Port attribué** | 8XXX | 8005 |
| **Adresse IP VM** | IP_VM | 192.168.1.100 |

---

## ⚡ Étape 1: Préparation - Construire & Publier l'Image Docker

### Sur votre machine locale (avec Docker installé):

```bash
# 1. Se positionner dans le répertoire du projet
cd /home/mo_benlamine/Downloads/medibook_project_f/medibook_project

# 2. Se connecter à Docker Hub (une seule fois)
docker login
# Entrer: username + password Docker Hub

# 3. Construire l'image
docker build -t votre_username/medibook:v1 .

# Exemple:
# docker build -t moncompte/medibook:v1 .

# 4. Publier sur Docker Hub
docker push votre_username/medibook:v1

# Exemple:
# docker push moncompte/medibook:v1

# 5. Vérifier sur Docker Hub
# Accéder à: https://hub.docker.com/r/votre_username/medibook
# ✅ Confirmer que l'image est listée
```

**Résultat attendu:**
```
✅ Image disponible sur Docker Hub: votre_username/medibook:v1
```

---

## ⚡ Étape 2: Connexion à Dokploy

### Accéder à Dokploy:

```
1. Ouvrir le navigateur
2. Aller à: http://IP_VM:3000
   (Remplacer IP_VM par l'adresse fournie par le professeur)
3. Connexion:
   - Identifiant: etudiant-XX
   - Mot de passe: ****
4. Cliquer sur "Sign In"
```

**Résultat attendu:**
```
✅ Accueil Dokploy affichée
```

---

## ⚡ Étape 3: Créer un Projet dans Dokploy

### Créer le projet:

```
1. Cliquer sur "Projects" (menu gauche)
2. Cliquer sur "Create Project"
3. Entrer le nom:
   medibook-etudiant-05
   (Remplacer 05 par votre numéro)
4. Cliquer "Create"
```

**Résultat attendu:**
```
✅ Projet créé
```

---

## ⚡ Étape 4: Créer et Configurer le Service Docker Compose

### Créer le service:

```
1. Dans le projet créé, cliquer "Add Service"
2. Choisir "Docker Compose"
3. Nom du service: medibook-app
4. Cliquer "Create"
```

### Configurer Docker Compose:

```
1. Copier le docker-compose.yml suivant:
```

```yaml
services:
  db:
    image: mysql:8.0
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD-SHELL", "mysqladmin ping -h localhost -u root -p$${MYSQL_ROOT_PASSWORD} || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 10

  web:
    image: votre_username/medibook:v1
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8005:8161"
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

**Modifications requises:**
- Remplacer `votre_username` par votre Docker Hub username
- Remplacer `8005` par le port attribué par le professeur

```
2. Coller dans le champ "Docker Compose"
3. Cliquer "Save"
```

**Résultat attendu:**
```
✅ Configuration sauvegardée
```

---

## ⚡ Étape 5: Ajouter les Variables d'Environnement

### Configuration des variables:

```
1. Aller à l'onglet "Environment"
2. Ajouter les variables suivantes:
```

| Clé | Valeur |
|-----|--------|
| `DJANGO_SECRET_KEY` | `your-secret-key-here-123456789` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `*` |
| `DB_ENGINE` | `mysql` |
| `MYSQL_ROOT_PASSWORD` | `root` |
| `MYSQL_DATABASE` | `medibook_db` |
| `MYSQL_USER` | `django` |
| `MYSQL_PASSWORD` | `django_password_123` |
| `MYSQL_HOST` | `db` |
| `MYSQL_PORT` | `3306` |
| `PORT` | `8161` |

```
3. Cliquer "Save"
```

**Résultat attendu:**
```
✅ Variables d'environnement configurées
```

---

## 🚀 Lancer le Déploiement

```
1. Cliquer sur "Deploy"
2. Attendre le déploiement (2-5 minutes)
3. Observer les logs qui s'affichent
```

**Logs attendus:**
```
Building image...
✅ Building complete
Running migrations...
✅ Applying migrations
Collecting static files...
✅ Static files collected
Starting Gunicorn...
✅ Server started
```

---

## ✅ Vérifier le Déploiement

### Vérifier les conteneurs:

```
1. Aller à "Containers"
2. Vérifier que les deux conteneurs sont GREEN:
   ✅ web (Django)
   ✅ db (MySQL)
3. Vérifier le statut "Healthy"
```

**Résultat attendu:**
```
✅ web: running ✓
✅ db: running ✓
```

---

## 🌍 Accéder à l'Application

### Ouvrir l'application:

```
1. Ouvrir le navigateur
2. Aller à: http://IP_VM:8005/
   (Remplacer 8005 par votre port attribué)
3. Tester les pages:
   - http://IP_VM:8005/               (Accueil)
   - http://IP_VM:8005/doctors/       (Médecins)
   - http://IP_VM:8005/patients/      (Patients)
   - http://IP_VM:8005/dashboard/     (Dashboard)
   - http://IP_VM:8005/admin/         (Admin)
```

**Résultat attendu:**
```
✅ Application accessible
✅ Toutes les pages chargent
```

---

## 👤 Créer un Superuser

### Accéder au terminal du conteneur:

```
1. Dans Dokploy, aller à Containers
2. Cliquer sur le conteneur "web"
3. Cliquer sur "Terminal"
4. Exécuter:
   python manage.py createsuperuser
5. Suivre les prompts:
   - Username: admin
   - Email: admin@example.com
   - Password: ****
6. Confirmer la création
```

### Accéder à l'administration:

```
1. Ouvrir: http://IP_VM:8005/admin/
2. Se connecter avec les identifiants créés
3. Vérifier que vous pouvez voir les tables (Doctors, Patients, etc.)
```

**Résultat attendu:**
```
✅ Superuser créé
✅ Admin accessible
```

---

## 🐛 Dépannage

### Si l'application ne démarre pas:

```
1. Vérifier les logs:
   Containers -> web -> Logs
   
2. Chercher les erreurs:
   - "Connection refused" → Vérifier les variables DB
   - "Table does not exist" → Vérifier les migrations
   - "Bad Request 400" → Vérifier ALLOWED_HOSTS
   
3. Solutions:
   - Modifier les variables d'environnement
   - Recliquer "Deploy"
   - Supprimer le volume db_data et redéployer
```

---

## 📝 Informations pour la Remise

Préparez:

- [ ] Lien GitHub du projet
- [ ] Nom complet de l'image Docker Hub (ex: moncompte/medibook:v1)
- [ ] URL finale de l'application (ex: http://192.168.1.100:8005/)
- [ ] Screenshots:
  - [ ] Docker Compose local fonctionnant
  - [ ] Dokploy avec conteneurs GREEN
  - [ ] Application accessible (page d'accueil)
  - [ ] Admin panel connecté

---

## 🎯 Résumé des Commandes

| Étape | Commande |
|-------|----------|
| Construire image | `docker build -t username/medibook:v1 .` |
| Publier image | `docker push username/medibook:v1` |
| Créer superuser | `python manage.py createsuperuser` |
| Voir logs | `Containers -> web -> Logs` |
| Accéder app | `http://IP_VM:PORT/` |

---

**✨ Félicitations!** Votre application Medibook est maintenant déployée sur Dokploy! 🎉

