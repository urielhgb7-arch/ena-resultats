# Plateforme de Résultats ENA

Bienvenue sur le dépôt de la plateforme de consultation et de gestion des résultats de l'ENA. Ce projet vise à moderniser, sécuriser et unifier le processus de publication et de consultation des notes pour les étudiants et l'administration.

## 🚀 Fonctionnalités Principales

- **Dashboard Admin 100% Personnalisé** : Interface d'administration en mode "Design Monster" (Glassmorphism, thèmes sombres) remplaçant totalement le Django Admin natif.
- **Gestion du Référentiel** : Interfaces CRUD complètes pour les Niveaux, Filières, Semestres et Unités d'Enseignement (UE).
- **Import de Résultats** : Système d'upload Drag & Drop pour les fichiers Excel de PV avec conservation de l'historique et de l'intégrité des notes.
- **Sécurité et Rôles** : Accès granulaires séparant les étudiants (consultation), les validateurs (import/gestion) et les super-administrateurs (configuration système).

## 🛠️ Stack Technique

- **Backend** : Django 5.x, Python 3.12
- **Base de données** : PostgreSQL 16
- **Frontend** : HTML5, Vanilla JS, Tailwind CSS (via CDN)
- **Conteneurisation** : Docker, Docker Compose

## 📚 Documentation Détaillée

Consultez les guides suivants pour approfondir l'architecture, l'utilisation ou le déploiement :
- [Architecture et Modèle de Données](docs/architecture.md)
- [Guide de Déploiement](docs/deployment.md)
- [Guide d'Utilisation](docs/usage.md)
- [Guide de Contribution](CONTRIBUTING.md)

## ⚡ Quickstart (Développement Local)

Le projet utilise Docker pour simplifier le lancement de l'environnement de développement.

1. **Cloner le dépôt**
   ```bash
   git clone <repo-url>
   cd ena-resultats
   ```

2. **Configuration**
   Copiez le fichier `.env.example` en `.env` :
   ```bash
   cp .env.example .env
   ```

3. **Lancer les conteneurs**
   ```bash
   docker-compose up -d
   ```

4. **Migrations et Super-Utilisateur**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

L'application sera accessible sur `http://localhost:8000/`.
