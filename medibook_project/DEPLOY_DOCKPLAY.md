# Déploiement sur Dockplay (Guide spécifique à MediBook)

Ce document complète les étapes recommandées (atelier PDF) et adapte la procédure au dépôt actuel.

Résumé rapide
- Utiliser `medibook_project/docker-compose.yml` (ou `docker-compose.yml` à la racine) pour Dockplay.
- Variables d'environnement: configurez via l'interface Dockplay ou variables secrètes (ne pas committer).
- Le conteneur `web` utilise `docker-entrypoint.sh` pour attendre la DB, lancer migrations, collectstatic, puis Gunicorn.

1) Pré-requis
- Avoir un dépôt Git public/privé accessible par Dockplay.
- S'assurer que `Dockerfile`, `docker-compose.yml`, `docker-entrypoint.sh`, et `.env.production` sont présents (ils le sont).
- Ne pas committer de `.env` contenant des secrets (vérifié et supprimé si nécessaire).

2) Vérifications dans le dépôt (actions à faire localement)
- Confirmer que `.gitignore` contient `.env` (présent dans `medibook_project/.gitignore`).
- Vérifier `docker-entrypoint.sh` : il exécute `migrate`, `collectstatic` et démarre Gunicorn (OK).
- Vérifier `docker-compose.yml` : le service `db` est `postgres:16-alpine`, volumes définis, healthchecks présents.

3) Variables d'environnement à définir dans Dockplay
Ajoutez au moins les variables suivantes (ou copiez `.env.production` dans l'UI de Dockplay):

- `DEBUG=False`
- `SECRET_KEY` = clé Django forte (générer via `python -c "from django.core.management.utils import get_random_secret_key(); print(...)"`)
- `ALLOWED_HOSTS` = votre domaine (ex: `myapp.dockplay.io`)
- `CSRF_TRUSTED_ORIGINS` = `https://<votre-domaine>`
- `DB_ENGINE=postgres`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST=db`, `DB_PORT=5432`
- `PORT=8161`
- `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_CONTENT_TYPE_NOSNIFF=True` (selon configuration HTTPS du proxy)

4) Configurer l'application sur Dockplay
- Créez une nouvelle application et pointez sur votre repository.
- Choisissez la méthode "Docker Compose" (ou équivalent Docker multi‑service) et vérifiez le chemin vers `docker-compose.yml` (utilisez `medibook_project/docker-compose.yml` si nécessaire).
- Définissez les variables d'environnement listées ci‑dessus.
- Définissez les volumes (si l'interface le demande) pour `postgres_data`, `staticfiles`, `media` — Dockplay gère souvent les volumes automatiquement.

5) Build & déploiement
- Lancez le déploiement via l'interface Dockplay. Dockplay va :
  - builder l'image `web` (contexte `.` ou `medibook_project/` selon votre compose);
  - lancer `db` (Postgres) et `web`.

6) Vérifications post‑déploiement
- Consulter les logs `web` et `db` depuis l'UI Dockplay.
- Vérifier que healthcheck `web` passe (port ${PORT}).
- Ouvrir l'URL publique : `https://<votre-app>`.
- Si erreurs de migrations, exécuter manuellement via l'interface ou corriger les variables et relancer.

7) CI/CD et build automatique
- Le dépôt contient un workflow GitHub Actions `/.github/workflows/ci-cd.yml` qui : installe dépendances, lance checks/tests et build Docker.
- Pour pousser l'image sur un registre (Docker Hub / GHCR), ajoutez un job `push` dans le workflow avec les secrets `DOCKER_USERNAME`, `DOCKER_PASSWORD` (ou `GITHUB_TOKEN` pour GHCR).

Exemple rapide (commande locale pour test)
```bash
# depuis le dossier racine du dépôt
docker compose -f medibook_project/docker-compose.yml up --build

# ouvrir http://localhost:8161
```

8) Bonnes pratiques sécurité
- Ne commitez jamais vos secrets. Utilisez `SECRET_KEY` et `DB_PASSWORD` via les variables d'environnement Dockplay.
- Rotater la `SECRET_KEY` si elle a fuité (voir `SECURITY_REMEDIATION.md`).
- Assurez-vous que `DEBUG=False` en production.

9) Problèmes courants & solutions
- Erreur: `psql` non disponible dans l'image : le `Dockerfile` du projet installe `postgresql-client` (vérifier). 
- Erreur: fichiers statiques manquants : vérifier que `collectstatic` s'est bien exécuté dans les logs du conteneur `web`.
- Erreur: boucle HTTPS : si Dockplay termine le TLS en proxy, garder `SECURE_SSL_REDIRECT=False` et veiller au header `X-Forwarded-Proto`.

10) Étapes optionnelles (avancées)
- Utiliser un registre d'images et déployer l'image pré‑buildée plutôt que de builder à chaque déploiement.
- Ajouter un job GitHub Actions pour builder et pousser l'image : utile pour rollback et audits.
- Configurer backups périodiques du volume Postgres (Dockplay fournit souvent des options ou utiliser `pg_dump` vers un stockage objet).

---

Si vous voulez, je peux :
- générer un exemple de job GitHub Actions pour builder et pousser l'image sur Docker Hub/GHCR ;
- ou lancer localement `docker compose` pour tester le déploiement ici et vérifier que l'app démarre (nécessite Docker installé sur votre machine).
