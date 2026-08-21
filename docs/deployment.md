# Guide de Déploiement

Ce document explique comment déployer l'application ENA Résultats sur un environnement de production ou de staging.

## Prérequis Système

Le déploiement recommandé s'appuie intégralement sur les conteneurs. Le serveur cible doit disposer de :
- Docker Engine
- Docker Compose v2+
- Une connexion sortante pour télécharger les dépendances (ou un registre d'images privé).

## Configuration de l'environnement

1. Clonez le dépôt sur le serveur de production.
2. Copiez le fichier `.env.example` en un fichier `.env`.
3. Configurez les variables de production critiques dans le `.env` :

```env
# Sécurité Django
DEBUG=False
SECRET_KEY=votre_cle_secrete_longue_et_aleatoire
ALLOWED_HOSTS=resultats.ena.ci,127.0.0.1

# Configuration PostgreSQL
POSTGRES_DB=ena_prod
POSTGRES_USER=ena_user
POSTGRES_PASSWORD=mot_de_passe_fort

# Configuration URL d'administration
ADMIN_URL_PATH=super-secret-admin/
```

> [!WARNING]
> En production, le `DEBUG` doit **absolument** être fixé à `False` pour éviter la fuite de variables d'environnement en cas de crash applicatif.

## Déploiement via Docker Compose

L'application est packagée avec un `Dockerfile` (image légère basée sur `python:3.12-slim`) qui embarque les librairies nécessaires (notamment `libpq-dev` et `gcc` pour compiler psycopg).

### 1. Construire et Lancer

Pour déployer l'application, placez-vous à la racine du projet et exécutez :

```bash
docker-compose up -d --build
```
*Le flag `--build` assure que toute modification de code ou de dépendances dans `requirements.txt` est prise en compte.*

### 2. Application des Migrations (Important)

Après le lancement initial ou lors du déploiement d'une nouvelle version comprenant des modifications de base de données :

```bash
docker-compose exec web python manage.py migrate
```

### 3. Rassembler les fichiers statiques (Staticfiles)

En production (DEBUG=False), Django ne sert plus directement les fichiers statiques. Il est impératif de les collecter pour qu'un proxy inverse (comme Nginx) puisse les exposer :

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

*(Note: Assurez-vous d'avoir configuré un reverse proxy (ex: Nginx ou Traefik) devant le conteneur Docker pour gérer les certificats SSL/TLS et servir le contenu du dossier `static/` et `media/`)*.

### 4. Création du compte d'administration initial

Si la base de données est vierge, générez le compte Super Administrateur :

```bash
docker-compose exec web python manage.py createsuperuser
```

## Sauvegardes de Base de Données

Les données Postgres sont persistées via un volume nommé défini dans `docker-compose.yml` (`pgdata`).
Pour créer un dump manuel de la base de données :

```bash
docker-compose exec db pg_dump -U ena_user ena_prod > backup_ena_$(date +%F).sql
```
