# Documentation de Sécurité

## Scan OWASP ZAP Baseline

Pour exécuter un scan de vulnérabilités sur l'environnement de staging déployé, utilisez la commande suivante avec OWASP ZAP :

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t <url-staging>
```

Remplacez `<url-staging>` par l'URL de votre environnement de test.

### Faux Positifs Attendus

*   *(À documenter au fur et à mesure des scans)*

---

## Checklist de Déploiement en Production (OWASP ASVS Niveau 2)

Avant toute mise en production, vérifiez manuellement les points suivants, issus du standard de sécurité :

### 1. Authentification et Mots de Passe
- [ ] Hashing des mots de passe via **Argon2** configuré en premier dans `PASSWORD_HASHERS`.
- [ ] Politique de mot de passe (`AUTH_PASSWORD_VALIDATORS`) complète : longueur minimale de 12 caractères, pas de mot de passe commun, ni similaire à l'identifiant.
- [ ] Limitation du taux de tentatives de connexion (`django-axes` ou équivalent) active (ex. verrouillage après 5 échecs).
- [ ] Aucun compte admin par défaut avec identifiants prévisibles.

### 2. Sessions et Cookies
- [ ] `SESSION_COOKIE_SECURE = True` et `CSRF_COOKIE_SECURE = True` (HTTPS obligatoire).
- [ ] `SESSION_COOKIE_HTTPONLY = True`.
- [ ] `SESSION_COOKIE_SAMESITE = "Lax"`.
- [ ] Expiration de session configurée (pas de session infinie pour les administrateurs).

### 3. Transport et En-têtes
- [ ] `SECURE_SSL_REDIRECT = True` actif en production.
- [ ] Paramètres HSTS activés (`SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`).
- [ ] Protection Clickjacking activée (`X_FRAME_OPTIONS = "DENY"`).
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True` activé.

### 4. Injection et Validation des Entrées
- [ ] Utilisation exclusive de l'ORM Django (pas de requêtes SQL brutes avec variables utilisateur).
- [ ] L'auto-échappement des templates Django n'est pas désactivé (`|safe` est restreint ou proscrit).
- [ ] Validation stricte des fichiers uploadés (import Excel) : vérification de l'extension, du type MIME, contrôle de la taille maximale (ex. 10 Mo) et stockage en dehors des répertoires servis publiquement.

### 5. Autorisation et Permissions
- [ ] Chaque vue admin/validateur vérifie les rôles **côté serveur** (ex: décorateurs ou mixins) et non uniquement dans les templates.
- [ ] Les vues Super-admin sont inaccessibles aux autres rôles, même par accès direct à l'URL (vérifié).
- [ ] Principe du moindre privilège appliqué au compte base de données (pas de rôle `superuser` Postgres pour l'app).

### 6. Secrets et Configuration
- [ ] Aucun secret codé en dur ; tout passe par les variables d'environnement (`.env`).
- [ ] `DJANGO_SECRET_KEY` est générée de manière sécurisée et aléatoire pour la production.
- [ ] **`DEBUG = False`** est strictement appliqué en production.

### 7. Dépendances
- [ ] `pip-audit` ou `safety` exécuté sur `requirements.txt` ; aucune vulnérabilité critique/haute non résolue.
- [ ] Versions des packages épinglées (pas de `>=` sans limite haute en production).

### 8. Journalisation et Audit
- [ ] Le journal d'activité (connexions, modifications, publications) fonctionne avec horodatage et identité de l'auteur.
- [ ] **Aucune journalisation en clair** de mots de passe, tokens ou de données personnelles sensibles dans les logs applicatifs.

### 9. Sauvegardes
- [ ] Un script de sauvegarde / restauration de la base de données est disponible et fonctionnel.

### 10. Vérification Finale
- [ ] La commande `python manage.py check --deploy` renvoie **zéro avertissement**.
