# Sécurité — Plateforme de résultats ENA

Ce document répertorie les consignes et les checklists nécessaires pour maintenir la sécurité de la plateforme, conformément aux exigences de l'OWASP ASVS niveau 2 et aux directives du Bureau d'Union des Entités de l'ENA.

## 1. Scan de Sécurité (OWASP ZAP Baseline)

Avant toute mise en production ou lors de modifications majeures, un scan de vulnérabilités doit être effectué contre l'environnement de staging.

### 1.1 Exécution du scan ZAP

Pour lancer un scan avec OWASP ZAP, exécutez la commande suivante en remplaçant `<url-staging>` par l'URL cible :

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t <url-staging>
```

### 1.2 Faux Positifs Attendus

*(À documenter au fur et à mesure des scans)*
- Aucun faux positif documenté pour le moment.

---

## 2. Checklist finale de mise en production (ASVS / Bureau)

Avant de livrer au Bureau, cette checklist **doit** être validée manuellement point par point. Chaque livraison de branche touchant `config/settings.py` doit d'abord passer la commande de vérification intégrée de Django.

### Exigences Générales
- [ ] La commande `python manage.py check --deploy` remonte **zéro avertissement**.

### 4.1 Authentification et mots de passe
- [ ] **Argon2** est configuré en premier dans `PASSWORD_HASHERS`.
- [ ] La politique de mot de passe (`AUTH_PASSWORD_VALIDATORS`) est complète (longueur min. 12, pas de MDP communs).
- [ ] La limitation de tentatives de connexion (rate limiting) est active et verrouille après 5 échecs.
- [ ] Aucun compte administrateur avec identifiants prévisibles n'est configuré par défaut.

### 4.2 Sessions et cookies
- [ ] `SESSION_COOKIE_SECURE = True` (HTTPS uniquement).
- [ ] `CSRF_COOKIE_SECURE = True` (HTTPS uniquement).
- [ ] `SESSION_COOKIE_HTTPONLY = True`.
- [ ] `SESSION_COOKIE_SAMESITE = "Lax"`.
- [ ] Une expiration de session raisonnable est définie.

### 4.3 Transport et en-têtes
- [ ] `SECURE_SSL_REDIRECT = True` est activé en production.
- [ ] `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS` et `SECURE_HSTS_PRELOAD` sont configurés.
- [ ] `X_FRAME_OPTIONS = "DENY"` (protection clickjacking).
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`.

### 4.4 Injection et validation des entrées
- [ ] Les requêtes à la BDD passent toutes par l'ORM Django (aucune injection SQL).
- [ ] Aucun auto-échappement de template (`|safe`) n'est utilisé sur du contenu non maîtrisé (protection XSS).
- [ ] Les fichiers uploadés sont validés sur l'extension **ET** le type MIME, limités en taille, et stockés hors du dossier public.

### 4.5 Autorisation et permissions
- [ ] Chaque vue admin/validateur vérifie explicitement son rôle **côté serveur**.
- [ ] Le principe de moindre privilège est appliqué pour la connexion base de données (pas de superuser Postgres).

### 4.6 Secrets et configuration
- [ ] **Aucun secret en dur dans le code**, la configuration repose sur les variables d'environnement (ex. `.env`).
- [ ] `DJANGO_SECRET_KEY` est générée aléatoirement en production.
- [ ] `DEBUG = False` en production (absolument obligatoire).

### 4.7 Dépendances
- [ ] Aucune vulnérabilité connue critique/haute dans les dépendances, validé par `pip-audit -r requirements.txt`.
- [ ] Les versions de packages sont épinglées en production.

### 4.8 Journalisation et audit
- [ ] Les événements sensibles (connexions, modifications, publications) sont journalisés.
- [ ] Les journaux applicatifs **ne contiennent aucun** mot de passe, token ou donnée personnelle sensible.

### 4.9 Sauvegardes
- [ ] Le script de dump/restauration de la base de données est présent et documenté.
