# Documentation de Sécurité

## OWASP ZAP Baseline Scan

Une fois l'environnement de staging déployé, vous pouvez exécuter un scan de vulnérabilités automatisé (OWASP ZAP baseline scan) en utilisant Docker :

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t <url-staging>
```

Remplacez `<url-staging>` par l'URL publique ou locale de votre environnement de staging.

### Faux positifs attendus
*Liste des faux positifs à documenter au fur et à mesure :*
- (À compléter lors des premiers scans)


## Checklist finale de mise en production

Avant chaque livraison en production, il est impératif de valider manuellement l'ensemble des points suivants, correspondant aux exigences de sécurité (§4).

### 4.1 Authentification et mots de passe
- [ ] Le hashing des mots de passe utilise **Argon2** (`django.contrib.auth.hashers.Argon2PasswordHasher` en premier dans `PASSWORD_HASHERS`).
- [ ] La politique de mot de passe (`AUTH_PASSWORD_VALIDATORS`) est complète (longueur minimale 12 caractères, mots de passe communs refusés, similitude avec l'identifiant refusée).
- [ ] Limitation du taux de tentatives de connexion (`django-axes` ou équivalent) active — verrouillage après 5 tentatives échouées.
- [ ] Aucun compte administrateur par défaut avec des identifiants prévisibles n'est présent en base.

### 4.2 Sessions et cookies
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_HTTPONLY = True`
- [ ] `SESSION_COOKIE_SAMESITE = "Lax"`
- [ ] Expiration de session raisonnable pour les comptes admin (pas de session infinie configurée).

### 4.3 Transport et en-têtes
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` activés.
- [ ] `X_FRAME_OPTIONS = "DENY"` (protection contre le clickjacking).
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`

### 4.4 Injection et validation des entrées
- [ ] Toutes les requêtes en base utilisent l'ORM Django (querysets). Aucun SQL brut.
- [ ] L'auto-échappement des templates Django n'est jamais désactivé via `|safe` sauf sur des contenus strictement contrôlés.
- [ ] Validation stricte des fichiers uploadés (ex: import Excel) : extension **ET** type MIME vérifiés, taille maximale imposée, stockage en dehors du dossier servi publiquement.

### 4.5 Autorisation et permissions
- [ ] Chaque vue admin/validateur vérifie le rôle côté serveur via des décorateurs/mixins (pas uniquement côté template).
- [ ] Un Validateur ne peut en aucun cas accéder aux vues réservées au Super-admin.
- [ ] Le compte de base de données utilisé par l'application respecte le principe du moindre privilège.

### 4.6 Secrets et configuration
- [ ] Aucun secret n'est codé en dur ; tout est géré via des variables d'environnement (`.env`).
- [ ] `DJANGO_SECRET_KEY` est généré aléatoirement et distinct pour la production.
- [ ] `DEBUG = False` est obligatoire en production (un check explicite est en place ou vérifié manuellement).

### 4.7 Dépendances
- [ ] Le script `scripts/security_check.sh` a été exécuté et `pip-audit` ne remonte aucune vulnérabilité haute/critique.
- [ ] Les versions des packages sont épinglées de manière stricte en production.

### 4.8 Journalisation et audit
- [ ] Le journal d'activité trace correctement les connexions, publications, modifications, suppressions (horodatage et auteur).
- [ ] Aucun mot de passe, token ou donnée personnelle sensible n'est journalisé en clair.

### 4.9 Sauvegardes
- [ ] Les scripts de dump/restauration de la base de données (et les backups automatiques) sont fonctionnels et testés.

### 4.10 Vérification finale automatique
- [ ] La commande `python manage.py check --deploy` remonte **zéro avertissement**.
- [ ] La commande `bandit -r apps/ config/` ne remonte aucun problème majeur.
