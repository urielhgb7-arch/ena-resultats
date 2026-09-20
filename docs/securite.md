# Documentation de Sécurité - Plateforme ENA

## Scan OWASP ZAP Baseline

Pour exécuter un scan de vulnérabilités contre l'environnement de staging, utilisez l'outil OWASP ZAP (Zed Attack Proxy) encapsulé dans Docker.

**Commande pour lancer le scan :**

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t <url-staging>
```

Remplacez `<url-staging>` par l'URL réelle de l'environnement de test ou staging.

### Faux positifs attendus

*À documenter ici au fur et à mesure que les scans identifient des éléments sans risque.*

- [Exemple : Missing Anti-clickjacking Header sur des pages statiques ou non sensibles non traitées par l'application (si le proxy en ajoute déjà)]
- ...

---

## Checklist de Déploiement en Production (ASVS niveau 2)

Avant toute mise en production, valider manuellement les points suivants :

### 4.1 Authentification et mots de passe
- [ ] Hashing des mots de passe via **Argon2** configuré en premier dans `PASSWORD_HASHERS`.
- [ ] Politique de mot de passe `AUTH_PASSWORD_VALIDATORS` complet.
- [ ] Limitation du taux de tentatives de connexion via `django-axes` (verrouillage après 5 échecs).
- [ ] Aucun compte admin par défaut ou avec des identifiants prévisibles.

### 4.2 Sessions et cookies
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_HTTPONLY = True`
- [ ] `SESSION_COOKIE_SAMESITE = "Lax"`
- [ ] Expiration de session raisonnable configurée.

### 4.3 Transport et en-têtes
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` activés.
- [ ] `X_FRAME_OPTIONS = "DENY"` (protection clickjacking).
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True` activé.

### 4.4 Injection et validation des entrées
- [ ] Utilisation exclusive de l'ORM Django (pas de SQL brut non échappé).
- [ ] Auto-échappement des templates non désactivé.
- [ ] Validation stricte des uploads (extension, MIME type et taille max imposée, stockage non public).

### 4.5 Autorisation et permissions
- [ ] Vérification des rôles côté serveur via décorateurs/mixins (Visiteur / Validateur / Super-admin).
- [ ] Isolation des accès testée (Validateur n'a pas accès aux vues Super-admin).
- [ ] Moindre privilège pour l'utilisateur DB (pas de superuser Postgres).

### 4.6 Secrets et configuration
- [ ] Aucun secret en dur dans le code ; utilisation stricte de `.env`.
- [ ] `DJANGO_SECRET_KEY` sécurisée et unique par environnement.
- [ ] `DEBUG = False` (vérifié et obligatoire).

### 4.7 Dépendances
- [ ] Exécution de `pip-audit -r requirements.txt` (pas de vulnérabilités non traitées).
- [ ] Versions des paquets épinglées.

### 4.8 Journalisation et audit
- [ ] Journal d'activité (logs via `django-simple-history`) actif.
- [ ] Aucun mot de passe ou PII loggé en clair.

### 4.9 Sauvegardes
- [ ] Dispositif de sauvegarde automatique en place ou script testé.

### 4.10 Vérification finale Django
- [ ] L'exécution de `python manage.py check --deploy` remonte 0 avertissement.
