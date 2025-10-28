# Portfolio Ultime - Application TodoList

Application Flask TodoList, dockerisée et déployée avec pipeline CI/CD.

L'application est conçue pour démontrer une architecture complète de développement moderne avec :

- **Containerisation** avec Docker
- **Base de données externe**
- **Migrations de schéma** avec Atlas
- **Pipeline CI/CD** automatisée
- **Tests multi-niveaux**
- **Déploiement Kubernetes** minimal

## Table des Matières

- [Aperçu du Projet](#aperçu-du-projet)
- [Pré-requis](#pré-requis)
- [Architecture Technique](#architecture-technique)
- [API Endpoints](#api-endpoints)
- [Schéma de Base de Données](#schéma-de-base-de-données)
- [Dépendances](#dépendances)
- [Configuration](#configuration)
- [Démarrage Rapide](#démarrage-rapide)
- [Containerisation Docker](#containerisation-docker)
- [Stratégie de Tests](#stratégie-de-tests-multi-niveaux)
- [Pipeline CI/CD](#pipeline-cicd)
- [Système de Versioning et Releases](#système-de-versioning-et-releases)
- [Déploiement Kubernetes](#déploiement-kubernetes)
- [Sécurité](#sécurité)
- [Licence](#licence)
- [TODO](#todo)

---

## Aperçu du Projet

Cette application TodoList permet de :

- ✅ Créer des tâches
- ✅ Consulter des tâches
- ✅ Marquer les tâches comme terminées/non terminées
- ✅ Supprimer des tâches
- ✅ Persister les données en base de données
- ✅ Interactions dynamiques sans rechargement de page

![Application TodoList](images/app.png)

---

## Pré-requis

- Secrets/Variables d'environnement GitHub :

| Type     | Nom                         | Description                                              |
| -------- | --------------------------- | -------------------------------------------------------- |
| Secret   | `NEON_API_KEY`              | Clé API Neon pour base de données éphémère (auto-généré) |
| Secret   | `PRIVATE_REGISTRY_PASSWORD` | Token GitHub pour GHCR (repo + package permissions)      |
| Secret   | `CONFIG_REPO_PAT`           | Token GitHub pour ArgoCD config repo (repo permissions)  |
| Variable | `NEON_PROJECT_ID`           | ID du projet Neon (auto-généré)                          |

- Token pour le repo infra : `ghcr-token` (read package permissions)

### Configuration de NEON_API_KEY et NEON_PROJECT_ID

L'accès à l'application GitHub est accordé exclusivement au dépôt "portfolio-ultime-app"

> **Note** : [Documentation GitHub Action de Neon Database](https://github.com/neondatabase/create-branch-action)

---

## Architecture Technique

### Stack Technologique

- **Frontend** : HTMX, Tailwind CSS v4, Alpine.js
- **Backend** : Flask (Python 3.13)
- **Base de données** : SQLite / PostgreSQL
- **ORM** : SQLAlchemy (Flask-SQLAlchemy)
- **Serveur WSGI** : Gunicorn
- **Containerisation** : Docker (build multi-stage et healthcheck)
- **Orchestration** : Kubernetes (Kind pour dev)

### Structure du Projet

```
portfolio-ultime-app/
├── app/                         # Code source de l'application Flask
│   ├── __init__.py              # Initialisation du package
│   ├── app.py                   # Point d'entrée principal
│   ├── requirements.txt         # Dépendances Python (app)
│   ├── models/
│   │   └── models.py            # Modèles SQLAlchemy (Todo)
│   ├── static/                  # Fichiers statiques
│   │   └── css/
│   │       ├── input.css        # Source Tailwind CSS
│   │       └── style.css        # CSS compilé (généré)
│   └── templates/               # Fichiers HTML (Jinja2)
│       ├── base.html            # Template principal
│       └── todo_list.html       # Template partiel (HTMX)
├── charts/                      # Chart Helm todolist pour déploiement Kubernetes
│   └── todolist/
│       ├── Chart.yaml           # Métadonnées Helm chart
│       ├── values.yaml          # Valeurs par défaut Helm
│       └── templates/
│           ├── deployment.yaml  # Déploiement K8s
│           ├── ingress.yaml     # Ingress K8s
│           └── service.yaml     # Service K8s
├── images/                      # Images illustratives (pour README)
├── instance/                    # Base SQLite locale (dev)
├── kubernetes/                  # Manifests pour le déploiement minimal
├── migrations/                  # Migrations Atlas (gérées automatiquement)
├── scripts/                     # Scripts pour CI et tests
│   ├── run-integration-tests.sh
│   ├── run-regression-tests.sh
│   ├── run-smoke-test.sh
│   └── run-units-tests.sh
├── tests/                       # Suite de tests automatisés
│   ├── conftest.py              # Fixtures et config pytest
│   ├── integration.py           # Tests d'intégration (Neon PostgreSQL)
│   ├── regression.py            # Tests de non-régression
│   ├── requirements-dev.txt     # Dépendances de test
│   └── units.py                 # Tests unitaires
├── atlas.hcl                    # Configuration Atlas pour migrations
├── Dockerfile                   # Build multi-stage Docker
├── pyproject.toml               # Config Python/Ruff
├── pytest.ini                   # Config pytest
├── README.md                    # Documentation principale
├── Taskfile.yaml                # Automatisation du cluster Kind
├── devbox.json                  # Config Devbox (dev local)
├── devbox-ci.json               # Config Devbox (CI)
├── devbox.lock                  # Lockfile Devbox
└── .github/
  └── workflows/               # Workflows GitHub Actions CI/CD
```

---

## API Endpoints

L'application expose les endpoints suivants :

| Endpoint       | Méthode | Description                          | Réponse                      |
| -------------- | ------- | ------------------------------------ | ---------------------------- |
| `/`            | GET     | Page d'accueil avec liste des tâches | HTML                         |
| `/add`         | POST    | Ajouter une nouvelle tâche           | HTML partiel (HTMX)          |
| `/update/<id>` | PUT     | Basculer l'état d'une tâche          | HTML partiel (HTMX)          |
| `/delete/<id>` | DELETE  | Supprimer une tâche                  | HTML partiel (HTMX)          |
| `/health`      | GET     | Health check                         | JSON `{"status": "healthy"}` |

> **Note** : L'application utilise **HTMX** pour les interactions dynamiques sans rechargement de page. Les endpoints `/add`, `/update`, et `/delete` retournent du HTML partiel qui met à jour uniquement la liste des todos.

---

## Schéma de Base de Données

### Modèle Todo

```sql
CREATE TABLE todos (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    complete BOOLEAN NOT NULL DEFAULT FALSE
);
```

**Champs :**

- `id` : Identifiant unique auto-incrémenté
- `title` : Titre de la tâche (max 100 caractères, requis)
- `complete` : Statut de completion (booléen, FALSE par défaut)

### Gestion des Migrations avec Atlas

L'application utilise [Atlas](https://atlasgo.io/) pour gérer les migrations de base de données de manière déclarative à partir des modèles SQLAlchemy.

#### Configuration

Le fichier `atlas.hcl` définit l'environnement **`postgres`** pour la gestion des migrations :

- **Source** : Modèles SQLAlchemy (`app/models/models.py`)
- **Dialecte** : PostgreSQL
- **Base dev** : Container Docker PostgreSQL 16 (pour génération des migrations)

#### Générer une Migration

Après avoir modifié les modèles dans `app/models/models.py` :

```bash
atlas migrate diff --env postgres
```

Cette commande :

- Compare les modèles SQLAlchemy avec les migrations existantes
- Génère automatiquement un fichier SQL dans `migrations/` si des changements sont détectés

**Fichiers générés :**

- `migrations/YYYYMMDDHHMMSS.sql` : Fichier de migration avec timestamp
- `migrations/atlas.sum` : Checksums pour validation d'intégrité

#### Appliquer les Migrations

```bash
atlas migrate apply --env postgres --url "$DATABASE_URL"
```

![Atlas-migrate](images/atlas-migrate.png)

**Important** : Pour NeonDB, il faut spécifier le schéma `public` dans l'URL (voir la partie Développement Local)

#### Inspecter le Schéma

```bash
atlas schema inspect --env postgres --url "$DATABASE_URL"
```

![Atlas-inspect](images/atlas-inspect.png)

#### Workflow Typique

1. **Modifier les modèles** dans `app/models/models.py`
2. **Générer la migration** : `atlas migrate diff --env postgres`
3. **Vérifier le fichier** de migration généré dans `migrations/`
4. **Appliquer la migration** : `atlas migrate apply --env postgres --url "$DATABASE_URL"`
5. **Commit** le fichier de migration dans Git

#### Intégration avec Kubernetes

L'application utilise l'[Atlas Kubernetes Operator](https://atlasgo.io/integrations/kubernetes) pour automatiser l'application du schéma lors des déploiements.

**Déploiement** : L'operator Atlas est installé automatiquement lors du déploiement Kubernetes via le `Taskfile.yaml`

**Configuration : `kubernetes/AtlasSchema.yaml`**

**Avantages** :

- ✅ Migrations automatiques au déploiement
- ✅ Gestion déclarative du schéma
- ✅ Synchronisation garantie entre modèles et base de données
- ✅ Rollback simplifié en cas de problème

#### Tests et CI/CD

- **Tests unitaires/régression** : Utilisent SQLite en mémoire avec `db.create_all()` (rapide, isolé, pas de migrations nécessaires)
- **Déploiement K8s** : L'Atlas Operator applique automatiquement le schéma de manière déclarative
- **Tests d'intégration** : Utilisent NeonDB
  - local : Faire la migration manuellement avant de lancer les tests
  - CI : Schéma déjà créé par Atlas Operator via K8s

> **Note** : Voir la [documentation officielle](https://atlasgo.io/guides/orms/sqlalchemy/getting-started) pour plus de détails.

---

## Dépendances

### Dépendances app (`app/requirements.txt`)

- **Flask** (3.1.2) : Framework web Python
- **Flask-SQLAlchemy** (3.1.1) : Extension SQLAlchemy pour Flask
- **psycopg2-binary** (2.9.10) : Driver PostgreSQL
- **Gunicorn** (23.0.0) : WSGI pour lancer l’application (via Dockerfile)
- **atlas-provider-sqlalchemy** (0.4.0) : Provider Atlas pour SQLAlchemy

### Dépendances tests (`tests/requirements-dev.txt`)

- **pytest** (8.4.2) : Framework de tests
- **pytest-flask** (1.3.0) : Plugin Flask pour pytest
- **pytest-cov** (6.0.0) : Couverture de code
- **pytest-html** (4.1.1) : Rapports HTML de tests

---

## Configuration

### Variables d'Environnement

- `DATABASE_URL` : URL de connexion base de données
  - SQLite : `sqlite:///todos.db` (par défaut)
  - PostgreSQL : `postgresql://user:pass@host:port/db`

### Healthcheck & Probes

- **Endpoints** : `/health`
- **Réponse** : JSON
- **Utilisation** : Docker, Kubernetes, monitoring

| Paramètre             | Readiness Probe (Vérification de disponibilité)                                                   | Liveness Probe (Vérification de santé)                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `initialDelaySeconds` | Attend 5 secondes avant de commencer à vérifier si le conteneur est prêt à recevoir du trafic.    | Attend 30 secondes avant de commencer à vérifier si le conteneur est en vie.                      |
| `timeoutSeconds`      | La vérification doit se terminer en 5 secondes maximum, sinon elle est considérée comme un échec. | La vérification doit se terminer en 5 secondes maximum, sinon elle est considérée comme un échec. |

---

## Démarrage Rapide

### Prérequis

- Python 3.13+
- Atlas CLI + NeonDB (pour les migrations des tests d'intégration)

### Développement Local

```bash
# Cloner le projet
git clone https://github.com/naqa92/portfolio-ultime-app.git
cd portfolio-ultime-app

# Setup environnement Python
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt

# Lancer l'application (SQLite par défaut)
cd app
python app.py

# Accéder à l'application
open http://localhost:5000
```

> **Note** :
>
> - En local, l'application utilise SQLite (`instance/todos.db`), créé automatiquement au premier lancement via `db.create_all()`.
> - Tailwind CSS CLI est installé via `devbox.json` pour la compilation des styles.

### Tests de Développement

```bash
# Installation dépendances de test
pip install -r tests/requirements-dev.txt

# Tests unitaires avec couverture (SQLite en mémoire)
cd tests && python -m pytest units.py --cov=../app --cov-report=html

# Tests de régression (SQLite en mémoire)
cd tests && python -m pytest regression.py -v

# Tests d'intégration (NeonDB URL avec search_path=public)
export DATABASE_URL="postgresql://user:password@host/db?sslmode=require&search_path=public"
atlas migrate diff --env postgres
atlas migrate apply --env postgres --url "$DATABASE_URL"
cd tests && python -m pytest integration.py -v --tb=short --html=../integration-test-report.html --self-contained-html

# Rapport HTML des tests
open units-test-report.html
open coverage-html/index.html
```

> _Pensez à nettoyer `.pytest_cache/` et `coverage-html/`_

---

## Containerisation Docker

Le `Dockerfile` utilise un build multi-stage pour optimiser la taille et la sécurité :

1. **Stage Builder** : Installation des dépendances Python
2. **Stage Production** : Image finale allégée avec :
   - Utilisateur non-root pour la sécurité
   - Healthcheck intégré (pour que l’image s’auto-contrôle)
   - Optimisations de taille

---

## Stratégie de Tests Multi-Niveaux

### Exécution des Tests

L'exécution des tests se fait via des scripts dédiés pour chaque niveau :

- **Unitaires** : `./scripts/run-units-tests.sh`
- **Intégration** : `./scripts/run-integration-tests.sh` (nécessite `$DATABASE_URL`)
- **Régression** : `./scripts/run-regression-tests.sh`
- **Smoke test Docker** : `./scripts/run-smoke-test.sh` (nécessite `$IMAGE` et `$NAME`)

Chaque script génère des rapports et affiche les résultats dans le terminal.

### 1. Linting avec Ruff

Ruff est un linter Python qui remplace plusieurs outils (flake8, isort, pycodestyle)

- Configuration via `pyproject.toml`

Report

![Ruff](images/ruff.png)

> **Note** : _Erreur E402 ignorée (import au niveau module qui n'est pas au début du fichier) dans les tests. C'est une pratique courante dans les tests, mais Ruff la signale comme une erreur._

### 2. Tests Unitaires avec code coverage (`tests/units.py`)

- ✅ Tests des routes Flask
- ✅ Tests du modèle Todo
- ✅ Tests CRUD de base
- ✅ Coverage minimum 80% (défini dans `.coveragerc`)

#### Flags utilisés

```bash
-v                   # Mode verbeux (affiche tous les tests)
--tb=short           # Traceback court pour les erreurs
--cov=../app         # Calcul de la couverture sur le dossier app
--cov-config=../.coveragerc   # Utilise la config de couverture définie
--cov-report=html:../coverage-html   # Génère un rapport HTML dans coverage-html
--cov-report=term    # Affiche la couverture dans le terminal
--html=../units-test-report.html   # Produit un rapport de tests HTML
--self-contained-html   # Fichier HTML autonome (inclut tout)
```

Report

![Units test](images/units-test.png)

Coverage

![Coverage](images/coverage.png)

### 3. Tests d'Intégration (`tests/integration.py`)

- ✅ Connexion base de données Neon
- ✅ Opérations CRUD réelles sur PostgreSQL
- ✅ Validation de la persistance

Report

![Integration test](images/integration-test.png)

Neon DB

![Neon DB](images/integration.png)

### 4. Tests de non régression (`tests/regression.py`)

Complémentaires aux tests unitaires existants

- ✅ Format des endpoints critiques : JSON
- ✅ Compatibilité schéma base de données (Vérification que la structure reste cohérente)
- ✅ Workflow end-to-end (Test rapide de l'intégration complète)
- ✅ Gestion des cas limites (Gestion des titres vides/espaces)

Report

![Regression test](images/regression-test.png)

### 5. CodeQL - SAST (`github/codeql-action/analyze@v3`)

CodeQL est le moteur d'analyse statique développé par GitHub qui excelle particulièrement dans l'écosystème GitHub Actions.

Avantages :

- ✅ Intégration native GitHub : Configuration automatique via la Security tab
- ✅ Analyse sémantique avancée : Traite le code comme une base de données interrogeable pour des analyses approfondies
- ✅ Taint tracking sophistiqué : Détecte les flux de données dangereux à travers les fonctions et fichiers
- ✅ Copilot Autofix : Suggestions de corrections automatiques pour les vulnérabilités détectées
- ✅ Analyse des workflows GitHub Actions : Détection des vulnérabilités spécifiques aux workflows CI/CD
- ✅ Support multi-langages : JavaScript, TypeScript, Python, Java, C#, C++, Go, Ruby

Le résultat du test se trouve dans : Security > Code scanning > Tools

![CodeQL](images/codeql.png)

> _Note: CodeQL est gratuit pour les dépôts publics. Pour les dépôts privés, il faut la licence Advanced Security (payant)_

> _Alternative : Bandit et Semgrep (Intégration de Bandit possible via Ruff : [doc](https://mcginniscommawill.com/posts/2025-01-25-intro-to-bandit/))_

### 6. Trivy - Container Security Scanning (`aquasecurity/trivy-action@0.33.1`)

Trivy est un scanner de sécurité complet qui analyse les images Docker pour détecter les vulnérabilités.

Avantages :

- ✅ Scanner multi-format : Images Docker, systèmes de fichiers, dépôts Git, Kubernetes manifests
- ✅ Base de données de vulnérabilités complète : CVE, OSV, GitHub Security Advisory
- ✅ Support multi-langages : Python, Node.js, Java, Go, Ruby, PHP, .NET, etc.
- ✅ Intégration GitHub Security : Upload SARIF automatique vers l'onglet Security
- ✅ Détection approfondie : OS packages, dépendances applicatives, fichiers de configuration
- ✅ Performance optimisée : Scan rapide avec cache intelligent

Configuration pipeline :

- **Format SARIF** : Résultats structurés pour intégration GitHub Security
- **Scan post-build** : Analyse de l'image Docker finale construite
- **Upload automatique** : Vulnérabilités visibles dans Security > Code scanning

Le scan s'exécute après la construction de l'image Docker et remonte automatiquement les vulnérabilités détectées dans l'onglet Security de GitHub.

![Trivy](images/trivy.png)

> _Alternative : Snyk pour génération automatique de PR avec fix de sécurité_

### 7. Smoke test Docker (`scripts/run-smoke-test.sh`)

Run de l'image Docker pour vérifier le health status (via docker inspect) qui reflète le résultat du HEALTHCHECK interne. (runner → container)

![Smoke test](images/smoke-test.png)

> **Note** : [Documentation](https://docs.docker.com/build/ci/github-actions/test-before-push/)

---

## Pipeline CI/CD

### GitHub Actions Workflow (`.github/workflows/ci.yaml`)

```mermaid
graph LR
    A[Push main] --> B[Job version]
    B --> C[Job CI]
    C --> D[Job release]
```

Le workflow CI/CD se déclenche sur les push vers la branche `main` et comprend 3 jobs séquentiels :

#### 1. **Job `version`** – Calcul de la version

- Récupère la version courante dans `pyproject.toml`
- Vérifie si un tag Git existe déjà pour cette version
- Si oui, incrémente automatiquement le PATCH (`0.1.0` → `0.1.1`)
- Sinon, publie la version courante

#### 2. **Job `ci`** – Lint, tests, build, scan, déploiement

Résumé des étapes principales :

- Linting avec Ruff
- Tests unitaires
- Tests de non régression
- Analyse SAST CodeQL (avec upload vers Security tab)
- Build image Docker
- Scan Trivy (avec upload vers Security tab)
- Smoke test Docker
- Push multi-plateforme (AMD64/ARM64) vers la registry Github (GHCR)
- Création branche Neon (PostgreSQL éphémère)
- Déploiement minimal Kubernetes (Kind + Helm)
- Tests d'intégration (Neon)
- Upload artefacts (rapports tests/couverture)
- Suppression branche Neon (cleanup)

#### 3. **Job `release`** – Publication coordonnée

- Met à jour tous les fichiers de version (`pyproject.toml`, `Chart.yaml`, `values.yaml`)
- Package et publie la chart Helm sur GHCR (OCI)
- Commit, tag et push la release Git
- Génère les notes de release automatiquement
- Met à jour le repo de config ArgoCD (image/tag Helm)

---

## Système de Versioning et Releases

### Fichiers Synchronisés

Le système maintient automatiquement la cohérence entre :

```bash
pyproject.toml          # version = "0.1.0"
charts/todolist/Chart.yaml     # version: 0.1.0 / appVersion: 0.1.0
charts/todolist/values.yaml    # image.tag: "0.1.0"
```

Les **Tags Git** et **GitHub Releases** sont ensuite automatiquement créés.

### Format de Versioning

**Semantic Versioning** : `MAJOR.MINOR.PATCH`

- **MAJOR** : Breaking changes
- **MINOR** : Nouvelles fonctionnalités
- **PATCH** : Auto-incrémenté à chaque commit

### Déclenchement des Releases

#### **Auto-incrémentation**

```bash
git add .
git commit -m "fix: resolve database connection issue"
git push
# → Version PATCH auto-incrémentée
```

#### **Versions manuelles**

```bash
sed -i 's/version = "0.1.0"/version = "0.2.0"/' pyproject.toml
git add pyproject.toml
git commit -m "bump: version 0.2.0"
git push
# → Utilise exactement la version 0.2.0
```

- **Auto-incrémentation** : Idéal pour le développement continu
- **Versions manuelles** : Pour les releases majeures/mineures planifiées

### Artifacts Publiés

Chaque release génère automatiquement :

| Artifact           | Localisation                                   | Format                       |
| ------------------ | ---------------------------------------------- | ---------------------------- |
| **Image Docker**   | `ghcr.io/naqa92/todolist:VERSION`              | Multi-platform (AMD64/ARM64) |
| **Chart Helm**     | `oci://ghcr.io/naqa92/charts/todolist:VERSION` | OCI Artifact                 |
| **Tag Git**        | `v0.1.0`                                       | Annotated tag avec notes     |
| **GitHub Release** | GitHub Releases                                | Changelog automatique        |

#### Notes de Release Automatiques

Chaque GitHub Release contient :

- **Artifacts coordonnés** avec leurs URLs
- **Changelog automatique** depuis le dernier tag

![Release Artifacts](images/release.png)

### Utilisation des Artifacts

#### **Déploiement Docker**

```bash
# Version spécifique
docker run ghcr.io/naqa92/todolist:0.1.0

# Dernière version
docker run ghcr.io/naqa92/todolist:latest
```

#### **Déploiement Helm**

```bash
# Installer depuis le registry OCI
helm install todolist oci://ghcr.io/naqa92/charts/todolist --version 0.1.0

# Lister les versions disponibles
helm search repo ghcr.io/naqa92/charts/todolist --versions
```

#### **Utilisation Helm en local**

```bash
helm template ./charts/todolist # Render
helm install todolist ./charts/todolist -n demo --create-namespace # Installation
helm upgrade todolist ./charts/todolist -n demo # Mise à jour
```

---

## Déploiement Kubernetes

### Déploiement Local avec Kind

```bash
# Créer cluster et déployer
task cluster-create

# Avec base de données externe
DATABASE_URL="postgresql://..." task cluster-create
```

- **kind.yaml** : exposition des ports 80 et 443
- **ingress-nginx** : activation du hostPort pour les ports 80 et 443
- **déploiement de l'app** : namespace, secret, deployment, service et ingress

![Minimal deployment](images/minimal-deployment.png)

> _Application accessible sur : todolist.127.0.0.1.nip.io (nip.io fonctionne en redirigeant 127.0.0.1.nip.io vers 127.0.0.1)_

---

## Sécurité

- **Utilisateur non-root** : L'image Docker utilise un utilisateur non-privilégié pour la sécurité
- **Health checks** : Endpoints de surveillance pour la disponibilité et la santé
- **Gestion des erreurs** : Rollback automatique des transactions DB en cas d'erreur
- **Validation des entrées** : Nettoyage des espaces dans les titres de tâches
- **Sécurité des conteneurs** : Build multi-stage réduisant la surface d'attaque
- **Méthodes HTTP appropriées** : Utilisation de POST/PUT/DELETE via HTMX pour les opérations RESTful

---

## Licence

Ce projet est sous licence MIT

---

## TODO

- Branch Protection : Blocage des push directs sur main (Review PR nécessaire)
- Passer à Snyk avec auto-génération de PR
- Monitoring - Métriques Prometheus/OpenTelemetry
