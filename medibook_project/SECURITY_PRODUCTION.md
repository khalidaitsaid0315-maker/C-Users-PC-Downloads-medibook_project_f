# Configuration securite production - MediBook

## Variables indispensables

Definissez ces variables dans Dokploy:

```env
DEBUG=False
SECRET_KEY=une-cle-django-forte-et-unique
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
CSRF_TRUSTED_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com

DB_ENGINE=postgres
DB_NAME=medibook_db
DB_USER=medibook_user
DB_PASSWORD=un-mot-de-passe-fort
DB_HOST=db
DB_PORT=5432
```

Generez une cle Django forte:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## HTTPS et proxy Dokploy

Dokploy termine generalement HTTPS au niveau du proxy. Dans ce cas, commencez avec:

```env
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

Activez `SECURE_SSL_REDIRECT=True` seulement si le proxy transmet correctement `X-Forwarded-Proto: https`, sinon l'application peut entrer dans une boucle de redirection.

## Secrets

Ne commitez jamais:

- `.env`
- mots de passe PostgreSQL reels
- cles API
- fichiers de sauvegarde de base de donnees

Les fichiers `.env.production` et `.env.dockplay` sont des modeles: remplacez toutes les valeurs avant le deploiement.
