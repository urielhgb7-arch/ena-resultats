# Documentation de Sécurité

## Scan OWASP ZAP Baseline

Pour lancer un scan OWASP ZAP baseline contre l'environnement de staging une fois déployé, utilisez la commande suivante (assurez-vous d'avoir Docker installé) :

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t <url-staging>
```

Remplacez `<url-staging>` par l'URL réelle de l'environnement de staging.

### Faux positifs attendus

Si le scan remonte des alertes qui s'avèrent être des faux positifs, veuillez les documenter ci-dessous avec leur justification :

- (Aucun faux positif documenté pour le moment. Ajoutez-les ici au fur et à mesure.)

## Checklist finale de mise en production

Avant toute livraison au Bureau, assurez-vous de vérifier manuellement chaque point ci-dessous :

### 1. Authentification et mots de passe
- [ ] Hashing des mots de passe via **Argon2** (`django.contrib.auth.hashers.Argon2PasswordHasher` en premier dans `PASSWORD_HASHERS`).
- [ ] Politique de mot de passe stricte (longueur minimale 12 caractères, pas de mot de passe commun, pas similaire à l'identifiant).
- [ ] **Limitation du taux de tentatives de connexion** (`django-axes` ou équivalent) - verrouillage après 5 tentatives échouées.
- [ ] Pas de compte admin par défaut avec identifiants prévisibles.

### 2. Sessions et cookies
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_HTTPONLY = True`
- [ ] `SESSION_COOKIE_SAMESITE = "Lax"`
- [ ] Expiration de session raisonnable pour les comptes admin.

### 3. Transport et en-têtes
- [ ] `SECURE_SSL_REDIRECT = True` en production.
- [ ] `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` activés.
- [ ] `X_FRAME_OPTIONS = "DENY"` (protection clickjacking).
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`

### 4. Injection et validation des entrées
- [ ] **Toujours** utiliser l'ORM Django (querysets), jamais de SQL brut.
- [ ] Auto-échappement des templates Django jamais désactivé (`|safe` interdit sauf contenu strictement contrôlé).
- [ ] Validation stricte de tout fichier uploadé (import Excel) : extension **et** type MIME vérifiés, taille maximale imposée, stockage hors du dossier servi publiquement.

### 5. Autorisation et permissions
- [ ] Chaque vue vérifie le rôle **côté serveur** via des décorateurs/mixins de permission systématiques.
- [ ] Un Validateur ne peut jamais accéder aux vues réservées Super-admin.
- [ ] Principe du moindre privilège pour l'utilisateur de base de données (pas de rôle superuser Postgres).

### 6. Secrets et configuration
- [ ] **Aucun secret en dur dans le code** — tout est dans `.env` (qui n'est pas commité).
- [ ] `DJANGO_SECRET_KEY` généré aléatoirement en production.
- [ ] `DEBUG = False` obligatoire en production.

### 7. Dépendances
- [ ] Exécuter **pip-audit** (ou `safety`) sur `requirements.txt` (aucune vulnérabilité de sévérité haute/critique non traitée).
- [ ] Versions de packages épinglées.

### 8. Journalisation et audit
- [ ] Le journal d'activité trace les connexions, publications, modifications, suppressions (horodatage + auteur).
- [ ] **Aucun mot de passe, token, ou donnée sensible** loggé en clair.

### 9. Sauvegardes
- [ ] Script de dump/restauration livré et documenté.

### 10. Vérification finale
- [ ] Exécution de `python manage.py check --deploy` remontant **zéro avertissement**.
