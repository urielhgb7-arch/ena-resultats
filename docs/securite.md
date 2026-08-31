# Documentation de Sécurité

## Scan OWASP ZAP Baseline

Pour lancer un scan OWASP ZAP baseline contre l'environnement de staging, utilisez la commande suivante :

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t <url-staging>
```

### Faux Positifs Attendus
*À documenter ici au fur et à mesure des scans.*

---

## Checklist de Mise en Production (OWASP ASVS niveau 2)

Avant chaque livraison au Bureau, vérifiez manuellement les points suivants :

- [ ] **Authentification et mots de passe**
  - Hashing Argon2 en premier dans `PASSWORD_HASHERS`.
  - Politique de mot de passe stricte (longueur min 12, pas commun, etc.).
  - Limitation du taux de tentatives de connexion (django-axes) : verrouillage après 5 échecs.
  - Aucun compte admin par défaut avec identifiants prévisibles.

- [ ] **Sessions et cookies**
  - `SESSION_COOKIE_SECURE = True` et `CSRF_COOKIE_SECURE = True` (HTTPS uniquement).
  - `SESSION_COOKIE_HTTPONLY = True`.
  - `SESSION_COOKIE_SAMESITE = "Lax"`.
  - Expiration de session raisonnable configurée.

- [ ] **Transport et en-têtes**
  - `SECURE_SSL_REDIRECT = True`.
  - HSTS activé (`SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`).
  - Protection clickjacking (`X_FRAME_OPTIONS = "DENY"`).
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`.

- [ ] **Injection et validation des entrées**
  - Utilisation exclusive de l'ORM (aucune requête SQL brute non sécurisée).
  - Auto-échappement des templates actif (pas de `|safe` sans contrôle absolu).
  - Validation stricte des fichiers uploadés (extension, type MIME, taille max 10 Mo, stockage sécurisé).

- [ ] **Autorisation et permissions**
  - Vérification du rôle côté serveur (décorateurs/mixins) pour chaque vue admin/validateur.
  - Test explicite interdisant l'accès d'un Validateur aux vues Super-admin.
  - Moindre privilège pour l'utilisateur de BDD (pas de superuser Postgres).

- [ ] **Secrets et configuration**
  - Aucun secret en dur (utilisation de `.env`).
  - `DJANGO_SECRET_KEY` fort et unique en production.
  - `DEBUG = False` (vérifié et obligatoire).

- [ ] **Dépendances**
  - Scan `pip-audit` ou `safety` passé avec succès (aucune vulnérabilité haute/critique).
  - Versions de packages épinglées.

- [ ] **Journalisation et audit**
  - Journal d'activité fonctionnel (connexions, modifications, etc. tracées).
  - Aucune donnée sensible (mot de passe, token) loggée en clair.

- [ ] **Sauvegardes**
  - Script de dump/restauration livré et documenté.

- [ ] **Vérification finale Django**
  - Commande `python manage.py check --deploy` exécutée avec **zéro avertissement**.
