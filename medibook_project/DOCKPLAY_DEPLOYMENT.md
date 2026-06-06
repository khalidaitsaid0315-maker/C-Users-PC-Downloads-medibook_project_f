# Guide de deploiement Dokploy - MediBook

Cette configuration deploie MediBook avec Docker Compose:

- `web`: application Django servie par Gunicorn
- `db`: PostgreSQL 16 avec volume persistant
- port applicatif par defaut: `8161`

## Fichiers prets pour Dokploy

- `Dockerfile`
- `docker-compose.yml`
- `docker-entrypoint.sh`
- `.env.production`
- `.dockerignore`

## Variables a configurer dans Dokploy

Ajoutez ces variables dans l'environnement de l'application, ou utilisez `.env.production` comme modele:

```env
DEBUG=False
SECRET_KEY=remplacez-par-une-cle-django-forte
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
CSRF_TRUSTED_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com

DB_ENGINE=postgres
DB_NAME=medibook_db
DB_USER=medibook_user
DB_PASSWORD=remplacez-par-un-mot-de-passe-fort
DB_HOST=db
DB_PORT=5432

PORT=8161
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

Si Dokploy termine le HTTPS sur son proxy, gardez `SECURE_SSL_REDIRECT=False` pour eviter les boucles de redirection. Activez-le seulement si le proxy transmet correctement `X-Forwarded-Proto: https`.

## Deploiement

1. Dans Dokploy, creez une application depuis le repository.
2. Choisissez Docker Compose comme methode de build/deploiement.
3. Verifiez que le chemin compose pointe vers `docker-compose.yml`.
4. Renseignez les variables d'environnement.
5. Lancez le deploiement.

Au demarrage, le conteneur `web` attend PostgreSQL, lance les migrations, collecte les fichiers statiques, puis demarre Gunicorn.

## Verification locale

```bash
docker compose up --build
```

Puis ouvrez:

```text
http://localhost:8161/
```

## Notes importantes

- Ne commitez jamais vos vraies valeurs `.env`.
- Changez `SECRET_KEY` et `DB_PASSWORD` en production.
- Les fichiers statiques sont servis par WhiteNoise.
- Les medias utilisateurs sont conserves dans le volume Docker `media`.
