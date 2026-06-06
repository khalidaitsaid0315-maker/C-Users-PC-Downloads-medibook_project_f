# Deploiement Dokploy en Raw Compose

En mode Raw Compose, Dokploy cree uniquement `docker-compose.yml`.
Il ne recoit pas le dossier Django, ni le `Dockerfile`.

Donc ce mode ne peut pas utiliser:

```yaml
build: .
```

Il faut utiliser une image Docker deja construite et publiee:

```yaml
image: votre-compte/medibook:latest
```

## Etapes

1. Construire l'image depuis la racine du projet:

```bash
docker build -t khalidaitsaid/medibook:latest .
```

2. Envoyer l'image vers Docker Hub:

```bash
docker login
docker push khalidaitsaid/medibook:latest
```

3. Dans Dokploy, coller le contenu de `docker-compose.raw.yml`.

4. Remplacer:

```text
khalidaitsaid/medibook:latest
```

par votre vraie image Docker.

5. Variables Dokploy recommandees:

```env
MEDIBOOK_IMAGE=khalidaitsaid/medibook:latest
DEBUG=False
SECRET_KEY=remplacez-par-une-cle-forte
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
CSRF_TRUSTED_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com
DB_NAME=medibook_db
DB_USER=postgres
DB_PASSWORD=remplacez-par-un-mot-de-passe-fort
PORT=8161
```
