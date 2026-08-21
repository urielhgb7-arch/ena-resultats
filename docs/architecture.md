# Architecture et Modèle de Données

Ce document décrit la structure interne de l'application, l'organisation des applications Django et le modèle de base de données relationnelle conçu pour gérer le référentiel académique et les résultats.

## Vue d'ensemble (Apps Django)

Le projet est découpé en plusieurs applications (apps) aux responsabilités métiers distinctes :

1. **`filieres`** : Gestion du référentiel académique de base.
2. **`resultats`** : Gestion des Unités d'Enseignement (UE), des Éléments Constitutifs (EC) et des notes.
3. **`imports`** : Mécanisme d'ingestion et de conservation de l'historique des fichiers de PV (Excel).
4. **`portail_admin`** : Vues de sécurité globales et architecture commune de l'interface d'administration (Mixins, layout centralisé).

---

## Modèle de Données (Base de Données)

L'architecture de la base de données est construite pour refléter l'organisation hiérarchique complexe de l'ENA et garantir la non-altération des notes une fois validées (PV signé).

### 1. Référentiel Académique (`apps.filieres`)

- **AnneeAcademique** : Représente l'année scolaire (ex: 2025-2026). Une seule année est généralement "active" à la fois.
- **Niveau** : Cycle d'étude (L1, L2, L3). Lié à une `AnneeAcademique`.
- **Filiere** : La filière métier (ex: Secrétariat, Diplomatie). Liée à un `Niveau`.
- **Specialite** : Option de spécialisation au sein d'une Filière.
- **Semestre** : Période temporelle académique (Semestre 1, Semestre 2, etc.) typée "normal" ou "stage".
- **SessionResultat** : Regroupe les évaluations d'une session (Normale, Rattrapage, Ajournement). Liée à un Semestre (et optionnellement à une Spécialité pour gérer le tronc commun).

### 2. Gestion des Notes et UEs (`apps.resultats`)

- **UE (Unité d'Enseignement)** : Matière principale avec un crédit alloué, attachée à une `SessionResultat`. Possède un statut de publication (Brouillon/Publié) et peut inclure un PDF d'archive du PV signé.
- **EC (Élément Constitutif)** : Sous-partie d'une UE, où les notes sont réellement saisies.
- **Etudiant** : Informations sur l'étudiant (Nom, Prénom, Matricule, Année promo).
- **NoteEC** : Note brute obtenue par un étudiant pour un EC spécifique. Toujours rattachée de manière traçable au fichier d'import d'origine (`ImportFichier`).
- **ResultatUE** : Représentation finale consolidée de la réussite d'un étudiant à une UE (Validé, Non validé).
  > [!IMPORTANT]  
  > **Règle métier stricte** : Le champ `moyenne_ue` est figé lors de l'import et correspond exactement au PV signé. Il ne doit **jamais** être recalculé dynamiquement à partir de `NoteEC`.

### 3. Gestion des Imports (`apps.imports`)

- **ImportFichier** : Entité de traçabilité qui sauvegarde chaque upload de fichier Excel. Elle trace l'auteur, le statut (Succès, Échec), le timestamp et maintient le fichier physique original pour un audit ultérieur.

---

## Modèles et Vues "Class-Based" (CBV)

Le projet favorise l'usage exclusif de Class-Based Views (ListView, CreateView, UpdateView, DeleteView) héritant d'un socle de sécurité commun :

- `AdminRequiredMixin` : Intercepte les requêtes pour s'assurer que l'utilisateur est soit membre du staff (Validateur), soit super-utilisateur. Empêche la modification accidentelle par des étudiants.
- L'historisation de chaque entité est assurée par `simple_history.models.HistoricalRecords`.

## Interfaces Personnalisées ("Design Monster")

La refonte visuelle abandonne le traditionnel Django Admin. L'interface utilise une approche `Glassmorphism` avec Tailwind CSS en CDN, pilotée depuis un layout maître :
- **Fichier maître** : `templates/portail_admin/base_dashboard.html`
- **UI Responsivité** : Les sidebars de navigation ont été transformées en composants "Drawer" masquables via Vanilla JS pour le support mobile.
