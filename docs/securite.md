# Sécurité de la plateforme de résultats ENA

Ce document répertorie les vérifications de sécurité nécessaires, le processus de test avec OWASP ZAP, et la checklist de déploiement avant mise en production, en conformité avec le brief de développement de l'agent.

## Scan OWASP ZAP Baseline

Pour lancer un scan OWASP ZAP baseline contre l'environnement de staging, utilisez la commande suivante (une fois déployé) :

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t <url-staging>
```

### Faux positifs attendus
*(À documenter au fur et à mesure)*

## Checklist de déploiement ASVS / OWASP Niveau 2

Avant de valider et déployer une nouvelle version en production, ces éléments doivent être obligatoirement vérifiés manuellement.

### 4.1 Authentification et mots de passe
- [ ] Hashing des mots de passe via **Argon2** (`django.contrib.auth.hashers.Argon2PasswordHasher` en premier dans `PASSWORD_HASHERS`).
- [ ] Politique de mot de passe : `AUTH_PASSWORD_VALIDATORS` complet (longueur minimale 12 caractères, pas de mot de passe commun, pas similaire à l'identifiant).
- [ ] Limitation du taux de tentatives de connexion (`django-axes` ou équivalent) : verrouillage après 5 tentatives échouées.
- [ ] Pas de compte admin par défaut avec identifiants prévisibles.

### 4.2 Sessions et cookies
- [ ] `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True` (HTTPS uniquement en production).
- [ ] `SESSION_COOKIE_HTTPONLY = True`.
- [ ] `SESSION_COOKIE_SAMESITE = "Lax"`.
- [ ] Expiration de session raisonnable pour les comptes admin (pas de session infinie).

### 4.3 Transport et en-têtes
- [ ] `SECURE_SSL_REDIRECT = True` en production.
- [ ] `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` activés.
- [ ] `X_FRAME_OPTIONS = "DENY"` (protection clickjacking).
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`.

### 4.4 Injection et validation des entrées
- [ ] Toujours utiliser l'ORM Django (querysets), **jamais de SQL brut** interpolé.
- [ ] Auto-échappement des templates Django activé (pas de `|safe` sans contrôle total de l'admin).
- [ ] Validation stricte des uploads (import Excel) : extension **ET** type MIME, taille max vérifiée, stockage hors du dossier public.

### 4.5 Autorisation et permissions
- [ ] Vérification du rôle **côté serveur** pour toutes les vues (admin/validateur/super-admin).
- [ ] Vérification qu'un validateur ne peut pas accéder aux vues super-admin (même en forgeant l'URL).
- [ ] Moindre privilège pour l'utilisateur de connexion BDD (pas de superuser postgres).

### 4.6 Secrets et configuration
- [ ] Aucun secret en dur dans le code (utiliser `.env`, `.env.example` fourni).
- [ ] `DJANGO_SECRET_KEY` fort, généré aléatoirement, différent des environnements de dev.
- [ ] `DEBUG = False` en production.

### 4.7 Dépendances
- [ ] Aucun vulnérabilité haute/critique remontée par `pip-audit` sur `requirements.txt`.
- [ ] Versions des packages épinglées.

### 4.8 Journalisation et audit
- [ ] Journal d'activité (historique) trace : connexions, publications, modifications, suppressions (horodatage + auteur).
- [ ] Aucun mot de passe, token, ni donnée sensible loggué en clair.

### 4.9 Sauvegardes
- [ ] Scripts de dump/restauration de la base de données présents (si applicable).

### 4.10 Vérification finale
- [ ] La commande `python manage.py check --deploy` remonte **zéro avertissement**.
