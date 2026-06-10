# 🐳 Build et Push Image Docker Hub (Sans GitHub)

## Prérequis
- Docker installé sur votre machine locale
- Compte Docker Hub (https://hub.docker.com)
- Username Docker Hub: **khalidaitsaid**

---

## Étape 1: Se Connecter à Docker Hub

```bash
docker login
```

**Prompts:**
```
Username: khalidaitsaid
Password: [Votre mot de passe Docker Hub]
```

**Résultat attendu:**
```
Login Succeeded
```

---

## Étape 2: Cloner/Copier le Projet

Assurez-vous d'avoir le projet localement:

```bash
cd /chemin/vers/medibook_project
```

**Fichiers nécessaires:**
- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `docker-entrypoint.sh`
- ✅ `medibook/` (dossier Django)
- ✅ `.env` ou variables d'environnement

---

## Étape 3: Construire l'Image

```bash
docker build -t khalidaitsaid/medibook:v1 .
```

**Logs attendus (2-3 minutes):**
```
[+] Building 45.2s (15/15) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [1/10] FROM python:3.11-slim
 => ...
 => exporting to image
 => => naming to docker.io/khalidaitsaid/medibook:v1
 => => sha256:abc123def456...
```

**Vérification:**
```bash
docker images | grep khalidaitsaid/medibook
```

**Résultat attendu:**
```
khalidaitsaid/medibook   v1        abc123def456   2 minutes ago   450MB
```

---

## Étape 4: Pousser l'Image vers Docker Hub

```bash
docker push khalidaitsaid/medibook:v1
```

**Logs attendus (2-5 minutes):**
```
The push refers to repository [docker.io/khalidaitsaid/medibook]
v1: digest: sha256:xyz789abc...
latest: digest: sha256:xyz789abc...
```

**Vérification:**
- Accéder à: https://hub.docker.com/r/khalidaitsaid/medibook
- Vérifier que l'image `v1` est listée ✅

---

## ✅ Image est Prête sur Docker Hub!

L'image `khalidaitsaid/medibook:v1` est maintenant disponible et peut être utilisée dans:
- **Docker Compose** localement
- **Dokploy** pour le déploiement

---

## Troubleshooting

### ❌ Error: "pull access denied"
- Vérifier que l'image a été poussée: `docker push khalidaitsaid/medibook:v1`
- Attendre 30-60 secondes que Docker Hub la rendre disponible

### ❌ Error: "no space left on device"
- Libérer de l'espace disque
- Supprimer les images inutilisées: `docker system prune -a`

### ❌ Error: "denied: requested access to the resource is denied"
- Vérifier que vous êtes connecté: `docker logout && docker login`
- Vérifier le username dans la commande build

---

## Prochaine Étape: Déployer sur Dokploy

Une fois l'image poussée, allez dans Dokploy et:
1. Créez un service Docker Compose
2. Collez le contenu de `docker-compose.dokploy.yml`
3. Cliquez **Deploy**
