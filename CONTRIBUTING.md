# Guide de contribution — Plateforme de résultats ENA

Ce document définit comment l'équipe travaille ensemble sur ce projet, du jour 1 jusqu'à la livraison. À lire avant ton premier commit.

---

## 1. Setup local (jour 1, 30 min max)

```bash
git clone <repo-url>
cd ena-resultats
cp .env.example .env        # remplir les valeurs (voir README pour la DB locale)
docker-compose up -d        # lance Postgres + l'app
python manage.py migrate
python manage.py createsuperuser
```

Si `docker-compose up` ne fonctionne pas chez toi après 10 minutes de debug, préviens dans le canal d'équipe au lieu de perdre ton temps seul — l'objectif est que tout le monde code dès le jour 1.

---

## 2. Stratégie de branches

**`main`** est protégée. Personne ne push directement dessus, pas même le tech lead. Tout passe par une Pull Request avec au moins 1 review.

**Pourquoi pas tout mettre sur `main` directement :**
- Une seule personne qui casse `main` bloque toute l'équipe derrière elle — sur 7 jours, tu n'as pas le temps de debug une régression collective.
- La review avant merge est le seul filet de sécurité qu'on a contre les bugs de logique (ex: un filtre de permission oublié — voir la discussion sur l'isolation des rôles).
- Un historique de PR propre est une partie du livrable documentaire attendu par le cahier des charges.

**Branches de travail :**
- Une branche par ticket/Issue, jamais une branche fourre-tout : `feature/modele-donnees`, `fix/navigation-stid`, `feat/auth-roles`
- Nommage : `<type>/<description-courte-en-kebab-case>`
- Tu pars toujours de `main` à jour (`git pull origin main` avant de créer ta branche)
- Durée de vie courte : une branche ouverte plus de 1-2 jours sur un sprint de 7 jours est un signal d'alerte — découpe le ticket plus petit si besoin

**Merge :**
- **Squash and merge** uniquement — garde l'historique de `main` lisible (1 commit = 1 feature complète)
- Supprime la branche après merge

---

## 3. Convention de commits

On utilise **Conventional Commits**, en anglais.

### Format
```
<type>(<scope>): <description courte, impératif, minuscule, sans point final>

[corps optionnel — explique le pourquoi]

[footer optionnel — ex: Closes #14]
```

### Types disponibles
| Type | Usage |
|---|---|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `refactor` | Réorganisation sans changement de comportement |
| `docs` | Documentation uniquement |
| `test` | Ajout/modification de tests |
| `chore` | Config, dépendances, CI |
| `style` | Formatage pur |
| `perf` | Optimisation de performance |

### Scopes du projet
`models`, `auth`, `admin`, `navigation`, `search`, `notifications`, `results`, `ci`

### Exemples
```
feat(models): add filiere, niveau, session entities
feat(auth): add visiteur/validateur/super-admin roles
fix(navigation): handle secretariat-gestion filiere without specialty
docs: add installation guide for staging environment
test(admin): add permission tests for validateur role scope
```

### Règles
1. Impératif présent : `add`, pas `added`
2. Une idée = un commit — ne mélange pas `feat` et `fix`
3. Référence l'Issue liée : `Closes #14` en footer ferme l'Issue au merge
4. Breaking change (rare ici) : `feat(auth)!: change role field type`

---

## 4. Process de Pull Request

1. Ouvre la PR dès que ta branche a du contenu, même incomplet — marque-la `[WIP]` dans le titre si ce n'est pas prêt à review. Ça permet à l'équipe de voir où en est chacun sans attendre le point de sync quotidien.
2. Description de PR minimale : quel ticket ça résout (`Closes #X`), ce qui a été testé manuellement.
3. **CI doit passer** (tests + linting) avant que le merge soit possible — configuré dès le jour 1 via GitHub Actions.
4. **1 review obligatoire minimum.** Sur les PR touchant modèle de données, auth, ou permissions : review par le tech lead systématiquement, priorité sur tout le reste.
5. Si tu reviews : teste localement si le changement touche une logique métier (pas juste lire le diff des yeux), surtout sur les cas d'exception (filières sans spécialité, ordre normal/rattrapage/ajournement).

---

## 5. Organisation du travail (kanban)

GitHub Projects avec colonnes : `Backlog` → `En cours` → `En review` → `Testé` → `Fait`

Chaque Issue = un scope + un préfixe de domaine dans le titre :
`[Backend] Modèle de données - entités filière/année/session`
`[Frontend] Navigation cascade filière→niveau→session`

Une personne s'assigne une Issue avant de commencer — évite que deux personnes travaillent le même ticket sans le savoir.

---

## 6. Rythme d'équipe

- **Sync quotidien 15 min max** : qui bloque, qui a une PR en attente de review depuis plus de quelques heures
- **Les 2-3 premiers jours** : le modèle de données (section 7 du cahier des charges) doit être figé et mergé en premier — tout le reste en dépend, front comme back. Pas de parallélisation sérieuse possible avant ça.
- **Jours 4-6** : développement parallèle des features une fois le socle stable
- **Jour 7** : gel des features, focus tests + jeu de données réel + documentation

---

## 7. Si un agent IA (Jules ou autre) contribue

Même règles que pour un humain : branche dédiée, PR avec description, CI qui passe, **review humaine obligatoire avant merge** — jamais de merge automatique même si les checks passent.
