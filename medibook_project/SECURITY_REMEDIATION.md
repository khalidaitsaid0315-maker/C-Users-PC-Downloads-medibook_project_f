Remediation pour secrets committés
--------------------------------

Actions recommandées après suppression du fichier `.env` contenant des secrets :

1. Faire un commit retirant le fichier :

   git rm medibook_project/.env
   git commit -m "Remove committed .env containing secrets"

2. Ajouter `.env` à `.gitignore` (déjà présent dans ce dépôt).

3. Révoquer/rotater la `SECRET_KEY` et tout mot de passe DB utilisé (changer sur l'environnement d'exécution).

4. Si le dépôt a été partagé publiquement, supprimer les secrets de l'historique Git :

   - Utiliser `git filter-repo` ou `git filter-branch` avec précaution.

5. Publier une nouvelle `ENV` sécurisée localement et ne pas la committer. Conserver un `.env.example` sans secrets.

6. Mettre à jour les secrets dans la plateforme d'hébergement (Dockplay, Render, etc.).

7. Ajouter une note dans la documentation de déploiement expliquant la procédure pour générer une nouvelle `SECRET_KEY` :

   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

8. Vérifier les autres fichiers de configuration pour ne pas exposer d'autres secrets.

Fin.
