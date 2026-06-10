# 🚀 DÉPLOIEMENT DOKPLOY - INSTRUCTIONS FINALES

## 📋 Fichiers à Utiliser

### 1️⃣ DOCKER COMPOSE RAW (à coller dans Dokploy)

```yaml
version: '3.8'

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
      test: ["CMD-SHELL", "mysqladmin ping -h localhost -u root -p$${MYSQL_ROOT_PASSWORD} || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 10

  web:
    image: mobenlamine/medibook:v1
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8061:8161"
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

---

### 2️⃣ VARIABLES D'ENVIRONNEMENT (à configurer dans Dokploy)

```env
SECRET_KEY=ND%cKAESQAdK`a~4uZPnhc`SA%gua7_8,onA5>&eExoDTh"idr
DEBUG=False
ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1,*.dockplay.io,IP_VM_DOKPLOY

DB_ENGINE=mysql
DB_NAME=medibook_db
DB_USER=django
DB_PASSWORD=django
DB_HOST=db
DB_PORT=3306

MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=medibook_db
MYSQL_USER=django
MYSQL_PASSWORD=django

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_SECURITY_POLICY=True

TIME_ZONE=Africa/Casablanca
LANGUAGE_CODE=fr-fr
PORT=8161
```

---

## ✅ ÉTAPES DE DÉPLOIEMENT SUR DOKPLOY

### Étape 1: Aller au Service Medibook

```
URL: http://IP_VM:3000/dashboard/proje...
Login avec: etudiant-XX
```

### Étape 2: Aller à l'onglet "Deployments"

Vous devriez voir le service qui a échoué. Cliquez sur le bouton "Redeploy" ou "Deploy".

### Étape 3: Remplacer le Docker Compose

1. Cliquez sur l'onglet **"General"**
2. Cherchez le champ **"Docker Compose"**
3. **Effacez tout** et **collez le Raw Docker Compose** (section 1️⃣ ci-dessus)
4. Cliquez **"Save"**

### Étape 4: Configurer les Variables d'Environnement

1. Cliquez sur l'onglet **"Environment"**
2. Pour chaque variable de la section 2️⃣, cliquez **"Add Variable"** et entrez:
   - Key: `SECRET_KEY`
   - Value: `ND%cKAESQAdK`a~4uZPnhc`SA%gua7_8,onA5>&eExoDTh"idr`
   
   *(Répétez pour toutes les variables)*

3. Cliquez **"Save"**

### Étape 5: Déployer

1. Allez à l'onglet **"Deployments"**
2. Cliquez le bouton **"Deploy"** (vert)
3. **Attendez 5-10 minutes** que les conteneurs démarrent

---

## 🔍 Vérifier le Déploiement

### Une fois le déploiement terminé:

```bash
# 1. Vérifier que les conteneurs tournent
curl -i http://IP_VM:8061/

# 2. Vous devriez avoir:
# HTTP/1.1 200 OK
# + Page MediBook HTML
```

### Si les conteneurs tournent mais la BD n'est pas initialisée:

```bash
# Accéder au conteneur web
docker exec -it medibook-app-web bash

# À l'intérieur du conteneur, exécuter:
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Créer un superuser (optionnel)
python manage.py createsuperuser
```

---

## 🆘 Troubleshooting

### ❌ "pull access denied for mobenlamine/medibook"
- Vérifier l'image sur Docker Hub: https://hub.docker.com/r/mobenlamine/medibook
- L'image `v1` doit être listée
- Attendre 1-2 min si juste poussée

### ❌ "Container exits with code 1"
- Vérifier les logs Dokploy (onglet "Logs")
- Vérifier variables d'environnement (DB_HOST, DB_PASSWORD, etc.)
- Vérifier que `DB_HOST=db` (pas localhost)

### ❌ "Connection refused on port 8061"
- Vérifier que le port 8061 est ouvert sur le firewall
- Vérifier que Dokploy écoute sur 0.0.0.0:8061

---

## 📝 Résumé Final

| Élément | Valeur |
|--------|--------|
| Image Docker | `mobenlamine/medibook:v1` |
| Base de Données | MySQL 8.0 |
| Port Application | `8061:8161` |
| Environment Variables | 25 variables (voir section 2️⃣) |
| Status | ✅ Prêt à déployer |

