# 🔧 Commandes Exactes pour Dokploy Deployment

## Étape 1: Sur Votre Machine Locale (Avec Docker)

### 1.1 Vérifier que Docker est installé

```bash
docker --version
docker compose --version
```

**Résultat attendu:**
```
Docker version 24.x.x, build xxxxx
Docker Compose version 2.x.x, build xxxxx
```

Si non installé → Installer Docker Desktop (https://www.docker.com/products/docker-desktop)

---

### 1.2 Naviguer vers le projet

```bash
cd /home/mo_benlamine/Downloads/medibook_project_f/medibook_project
```

---

### 1.3 Se Connecter à Docker Hub

```bash
docker login
```

**Prompts:**
```
Login with your Docker ID to push and pull images from Docker Hub. 
If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: [VOTRE_USERNAME]
Password: [VOTRE_PASSWORD]
```

**Résultat attendu:**
```
Login Succeeded
```

---

### 1.4 Construire l'Image (2-3 minutes)

**Option A: Avec script helper (recommandé)**

```bash
chmod +x build-and-push.sh
./build-and-push.sh votre_username
```

Remplacer `votre_username` par votre username Docker Hub.

**Option B: Commandes manuelles**

```bash
docker build -t votre_username/medibook:v1 .
```

Exemple:
```bash
docker build -t moncompte/medibook:v1 .
```

**Logs attendus:**
```
[+] Building 45.2s (15/15) FINISHED
 => [internal] load build definition from Dockerfile
 => ...
 => exporting to image
 => => naming to docker.io/moncompte/medibook:v1
```

---

### 1.5 Publier l'Image sur Docker Hub (2-5 minutes)

**Option A: Avec script helper**

Le script s'arrête après la publication. ✅

**Option B: Manuellement**

```bash
docker push votre_username/medibook:v1
```

Exemple:
```bash
docker push moncompte/medibook:v1
```

**Logs attendus:**
```
The push refers to repository [docker.io/moncompte/medibook]
v1: digest: sha256:xxx...
```

**Vérification:**
- Accéder à: https://hub.docker.com/r/votre_username/medibook
- Vérifier que l'image `v1` est listée ✅

---

## Étape 2: Sur Dokploy (Via Navigateur)

### 2.1 Se Connecter à Dokploy

```
1. Ouvrir dans le navigateur: http://IP_VM:3000
   (Remplacer IP_VM par l'adresse fournie par le professeur)

2. Entrer identifiants:
   Username: etudiant-XX
   Password: [mot de passe reçu]

3. Cliquer "Sign In"
```

**Résultat attendu:** Page d'accueil Dokploy affichée

---

### 2.2 Créer un Projet

```
1. Menu gauche: Cliquer sur "Projects"
2. Cliquer sur "Create Project"
3. Entrer le nom: medibook-etudiant-05
   (Remplacer 05 par votre numéro)
4. Cliquer "Create"
```

**Résultat attendu:** Projet créé

---

### 2.3 Créer un Service Docker Compose

```
1. Dans le projet créé: Cliquer "Create Service"
2. Choisir "Docker Compose"
3. Service name: medibook-app
4. Cliquer "Create"
```

**Résultat attendu:** Formulaire de configuration affichée

---

### 2.4 Configurer le Docker Compose

```
1. Dans le champ "Docker Compose", remplacer par:
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
    image: moncompte/medibook:v1
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
- Remplacer `moncompte` par **votre username Docker Hub** ✅
- Remplacer `8005` par **votre port attribué** (ex: 8001, 8002, etc.)

```
2. Cliquer "Save"
```

**Résultat attendu:** Configuration sauvegardée

---

### 2.5 Configurer les Variables d'Environnement

```
1. Aller à l'onglet "Environment"
2. Cliquer "Add Variable"
3. Ajouter chaque variable:
```

| Clé | Valeur | Notes |
|-----|--------|-------|
| `DJANGO_SECRET_KEY` | `your-secret-key-12345-change-me` | Générer une nouvelle clé |
| `DJANGO_DEBUG` | `False` | Production mode |
| `DJANGO_ALLOWED_HOSTS` | `*` | Permet tous les hosts |
| `DB_ENGINE` | `mysql` | Utilise MySQL |
| `MYSQL_ROOT_PASSWORD` | `root` | Défaut pour MySQL root |
| `MYSQL_DATABASE` | `medibook_db` | Nom de la base |
| `MYSQL_USER` | `django` | Utilisateur Django |
| `MYSQL_PASSWORD` | `django_secure_pass` | Mot de passe Django user |
| `MYSQL_HOST` | `db` | Nom du service Docker |
| `MYSQL_PORT` | `3306` | Port MySQL standard |
| `PORT` | `8161` | Port Django interne |

```
4. Cliquer "Save" après chaque ajout
```

**Résultat attendu:** Toutes les variables listées

---

### 2.6 Lancer le Déploiement

```
1. Cliquer sur "Deploy"
2. Attendre les logs...
```

**Logs attendus (2-5 minutes):**
```
Building image...
Running migrations...
Collecting static files...
Starting Gunicorn...
```

**Résultat attendu:** Déploiement complété

---

### 2.7 Vérifier les Conteneurs

```
1. Menu: Cliquer sur "Containers"
2. Vérifier les deux conteneurs:
   - db: Status "running" ✅
   - web: Status "running" ✅
3. Vérifier les healthchecks: "healthy" ✅
```

**Résultat attendu:** Deux conteneurs verts

---

## Étape 3: Accéder à l'Application

### 3.1 Ouvrir dans le Navigateur

```
Accéder à: http://IP_VM:PORT/
```

Où:
- `IP_VM` = l'adresse IP fournie par le professeur (ex: 192.168.1.100)
- `PORT` = votre port attribué (ex: 8005)

Exemple complet:
```
http://192.168.1.100:8005/
```

**Résultat attendu:** Page d'accueil Medibook s'affiche ✅

---

### 3.2 Tester les Pages

```
Accueil:         http://IP_VM:8005/
Médecins:        http://IP_VM:8005/doctors/
Patients:        http://IP_VM:8005/patients/
Dashboard:       http://IP_VM:8005/dashboard/
Admin:           http://IP_VM:8005/admin/
```

**Résultat attendu:** Toutes les pages chargent ✅

---

## Étape 4: Créer un Superuser

### 4.1 Accéder au Terminal du Conteneur

```
1. Dans Dokploy, menu "Containers"
2. Cliquer sur le conteneur "web"
3. Cliquer sur "Terminal"
4. Terminal s'ouvre
```

**Résultat attendu:** Terminal avec prompt `bash-5.x$`

---

### 4.2 Créer le Superuser

Dans le terminal, exécuter:

```bash
python manage.py createsuperuser
```

**Prompts:**
```
Username: admin
Email: admin@example.com
Password: [votre_mot_de_passe]
Password (again): [confirmer]
```

**Résultat attendu:**
```
Superuser created successfully.
```

---

### 4.3 Accéder à l'Admin

```
1. Ouvrir: http://IP_VM:8005/admin/
2. Se connecter:
   Username: admin
   Password: [le mot de passe que vous avez rentré]
3. Cliquer "Sign In"
```

**Résultat attendu:** Dashboard admin affichée ✅

---

## 🚨 Si Quelque Chose Ne Fonctionne Pas

### 4.4 Consulter les Logs

```
1. Dans Dokploy, menu "Containers"
2. Cliquer sur "web"
3. Cliquer sur "Logs"
4. Voir les messages d'erreur
```

**Erreurs courantes:**
- `Bad Request 400` → Variable `ALLOWED_HOSTS` incorrect
- `500 Server Error` → DB connection issue ou migrations
- `Table does not exist` → Migrations non appliquées
- `Connection refused` → Service MySQL/PostgreSQL pas prêt

### 4.5 Redéployer

```
1. Corriger les variables d'environnement
2. Cliquer "Deploy" à nouveau
3. Attendre la fin du déploiement
```

---

## 📋 Résumé des Commandes Principales

| Action | Commande |
|--------|----------|
| Connecter Docker | `docker login` |
| Construire image | `docker build -t username/medibook:v1 .` |
| Publier image | `docker push username/medibook:v1` |
| Créer superuser | `python manage.py createsuperuser` |
| Voir logs Dokploy | Containers -> web -> Logs |
| Accéder app | `http://IP_VM:PORT/` |
| Accéder admin | `http://IP_VM:PORT/admin/` |

---

## ✅ Checklist Finale

- [ ] Docker installé et testé
- [ ] Image construite localement
- [ ] Image publiée sur Docker Hub
- [ ] Connecté à Dokploy
- [ ] Projet créé dans Dokploy
- [ ] Service Docker Compose créé
- [ ] Variables d'environnement configurées
- [ ] Déploiement lancé et complété
- [ ] Conteneurs en GREEN
- [ ] Application accessible
- [ ] Superuser créé
- [ ] Admin fonctionnel
- [ ] Fichiers remis

---

**Bon déploiement! 🚀**

