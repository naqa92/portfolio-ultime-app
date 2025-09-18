# Portfolio Ultime - Application TodoList

Application Flask TodoList, dockerisée et déployée avec pipeline CI/CD.

L'application est conçue pour démontrer une architecture complète de développement moderne avec :

- **Containerisation** avec Docker (build multi-stage et healthcheck)
- **Base de données externe** (Neon PostgreSQL)
- **Pipeline CI/CD** automatisée
- **Tests multi-niveaux** (unitaires, intégration, régression)
- **Déploiement Kubernetes** minimal

## 🚀 Aperçu du Projet

Cette application TodoList permet de :

- ✅ Créer des tâches
- ✅ Consulter des tâches
- ✅ Marquer les tâches comme terminées/non terminées
- ✅ Supprimer des tâches
- ✅ Persister les données en base de données (SQLite/PostgreSQL)

> **Note** : Les formulaires HTML standards ne supportent que les méthodes GET et POST. Les opérations de mise à jour et de suppression utilisent donc la méthode GET.

## 🏗️ Architecture Technique

### Stack Technologique

- **Backend** : Flask (Python 3.13)
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **ORM** : SQLAlchemy avec Flask-SQLAlchemy
- **Serveur WSGI** : Gunicorn
- **Frontend** : HTML/CSS
- **Containerisation** : Docker avec build multi-stage
- **Orchestration** : Kubernetes (Kind pour dev)

### Structure du Projet

```
portfolio-ultime/
├── app/                      # Code source de l'application Flask
│   ├── app.py                # Point d'entrée principal
│   ├── templates/            # Fichiers HTML
│   └── requirements.txt      # Dépendances Python
├── tests/                    # Suite de tests automatisés
│   ├── units.py              # Tests unitaires
│   ├── integration.py        # Tests d'intégration (PostgreSQL)
│   ├── regression.py         # Tests de non-régression
│   └── conftest.py           # Fixtures et config pytest
├── scripts/                  # Scripts pour CI et tests
├── charts/                   # Chart Helm pour déploiement Kubernetes (déploiement, service, ingress)
├── Dockerfile                # Build multi-stage Docker
├── .github/workflows/        # Workflows GitHub Actions CI/CD
├── Taskfile.yaml             # Automatisation via Task
└── devbox-ci.json            # Configuration Devbox pour CI
```

---

## 🐳 Containerisation Docker

Le `Dockerfile` utilise un build multi-stage pour optimiser la taille et la sécurité :

1. **Stage Builder** : Installation des dépendances Python
2. **Stage Production** : Image finale allégée avec :
   - Utilisateur non-root pour la sécurité
   - Healthcheck intégré (pour que l’image s’auto-contrôle)
   - Optimisations de taille

## 🧪 Stratégie de Tests Multi-Niveaux

### 1. Linting avec Ruff

Ruff est un linter Python qui remplace plusieurs outils (flake8, isort, pycodestyle)

- ✅ Configuration via `pyproject.toml`

> **Note** : Erreur E402 ignorée (import au niveau module qui n'est pas au début du fichier) dans les tests. C'est une pratique courante dans les tests, mais Ruff la signale comme une erreur.

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

### 3. Tests d'Intégration (`tests/integration.py`)

- ✅ Connexion base de données Neon
- ✅ Opérations CRUD réelles sur PostgreSQL
- ✅ Validation de la persistance

#### Configuration de NEON_API_KEY

L'accès à l'application GitHub est accordé exclusivement au dépôt "portfolio-ultime"

> **Note** : [Documentation GitHub Action de Neon Database](https://github.com/neondatabase/create-branch-action)

### 4. Tests de non régression (`tests/regression.py`)

Complémentaires aux tests unitaires existants

- ✅ Format des endpoints critiques : JSON
- ✅ Compatibilité schéma base de données (Vérification que la structure reste cohérente)
- ✅ Workflow end-to-end (Test rapide de l'intégration complète)
- ✅ Gestion des cas limites (Gestion des titres vides/espaces)

### 5. Smoke test Docker (`scripts/run-smoke-test.sh`)

Run de l'image Docker pour vérifier le health status (via docker inspect) qui reflète le résultat du HEALTHCHECK interne. (runner → container)

> **Note** : [Documentation](https://docs.docker.com/build/ci/github-actions/test-before-push/)

### Exécution des Tests

L'exécution des tests se fait via des scripts dédiés pour chaque niveau :

- **Unitaires** : `./scripts/run-units-tests.sh`
- **Intégration** : `./scripts/run-integration-tests.sh` (nécessite `DATABASE_URL`)
- **Régression** : `./scripts/run-regression-tests.sh`
- **Smoke test Docker** : `./scripts/run-smoke-test.sh` (nécessite `IMAGE` et `NAME`)

Chaque script génère des rapports et affiche les résultats dans le terminal.

## 🔄 Pipeline CI/CD

### GitHub Actions Workflow (`.github/workflows/ci.yaml`)

La pipeline automatisée inclut :

1. **🔍 Analyse de Code**

   - Linting avec Ruff
   - Standards de qualité Python

2. **🧪 Tests Automatisés**

   - Tests unitaires avec coverage HTML
   - Tests de non régression
   - Génération de rapports

3. **🐳 Build & Test Docker**

   - Build multi-platform (AMD64/ARM64)
   - Smoke test de l'image
   - Push vers GitHub Container Registry

4. **🗄️ Base de Données Éphémère**

   - Création branche Neon temporaire
   - Tests d'intégration avec PostgreSQL
   - Nettoyage automatique

5. **☸️ Déploiement Minimal**

   - Cluster Kind temporaire
   - Déploiement Kubernetes
   - Validation du déploiement

6. **📊 Rapports & Artefacts**
   - Rapports de tests HTML
   - Coverage report
   - Artefacts conservés 7 jours

### Configuration Requise

Variables d'environnement GitHub :

```bash
# Secrets
NEON_API_KEY          # Clé API Neon pour DB éphémère
PRIVATE_REGISTRY_PASSWORD  # Token GitHub pour GHCR

# Variables
NEON_PROJECT_ID       # ID du projet Neon
```

## 🏷️ Système de Versioning et Releases

### Architecture du Versioning

Le projet utilise un système de versioning automatisé coordonné qui synchronise :

- **Python package** (`pyproject.toml`)
- **Image Docker** (GHCR)
- **Chart Helm** (GHCR OCI)
- **Tags Git** et **GitHub Releases**

### Workflow de Release Automatique

```mermaid
graph LR
    A[Push main] --> B[Job version]
    B --> C[Job CI + tests]
    C --> D[Job release]
    D --> E[GitHub Release]
```

Le workflow de release se compose de 3 jobs séquentiels :

#### 1. **Job `version`** - Calcul de la Version

- 📝 Lit la version actuelle depuis `pyproject.toml`
- 🔍 Vérifie si un tag Git existe déjà pour cette version
- 🔄 Si le tag existe : auto-incrémente le PATCH (`0.1.0` → `0.1.1`)
- ✅ Si nouveau : utilise la version du fichier

#### 2. **Job `ci`** - Tests et Build

- 🧪 Exécute tous les tests (unitaires, régression, intégration)
- 🐳 Build les images Docker avec tags `latest` + version
- 📦 Push vers GitHub Container Registry

#### 3. **Job `release`** - Publication Coordonnée

- 📝 Met à jour tous les fichiers avec la nouvelle version
- ⎈ Package et publie la chart Helm vers GHCR
- 🏷️ Crée le tag Git et la GitHub Release
- 📋 Génère les notes de release automatiquement

### Format de Versioning

**Semantic Versioning** : `MAJOR.MINOR.PATCH`

- **MAJOR** : Changements incompatibles
- **MINOR** : Nouvelles fonctionnalités compatibles
- **PATCH** : Corrections de bugs (auto-incrémenté)

### Déclenchement des Releases

#### **Release Automatique** (Recommandé)

```bash
# 1. Modifier le code
git add .
git commit -m "feat: nouvelle fonctionnalité"

# 2. Push sur main
git push origin main

# → La release se déclenche automatiquement
# → Version PATCH auto-incrémentée si nécessaire
```

#### **Release Manuelle avec Version Spécifique**

```bash
# 1. Modifier la version dans pyproject.toml
sed -i 's/version = "0.1.0"/version = "0.2.0"/' pyproject.toml

# 2. Commit et push
git add pyproject.toml
git commit -m "bump: version 0.2.0"
git push origin main

# → Utilise exactement la version 0.2.0
```

### Artifacts Publiés

Chaque release génère automatiquement :

| Artifact           | Localisation                                   | Format                       |
| ------------------ | ---------------------------------------------- | ---------------------------- |
| **Image Docker**   | `ghcr.io/naqa92/todolist:VERSION`              | Multi-platform (AMD64/ARM64) |
| **Chart Helm**     | `oci://ghcr.io/naqa92/charts/todolist:VERSION` | OCI Artifact                 |
| **Tag Git**        | `v0.1.0`                                       | Annotated tag avec notes     |
| **GitHub Release** | GitHub Releases                                | Changelog automatique        |

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

#### **Référencer une Version Git**

```bash
# Checkout d'une version spécifique
git checkout v0.1.0

# Voir toutes les versions
git tag -l "v*"
```

### Fichiers Synchronisés

Le système maintient automatiquement la cohérence entre :

```bash
pyproject.toml          # version = "0.1.0"
charts/todolist/Chart.yaml     # version: 0.1.0 / appVersion: 0.1.0
charts/todolist/values.yaml    # image.tag: "0.1.0"
```

### Notes de Release Automatiques

Chaque GitHub Release contient :

- **Artifacts coordonnés** avec leurs URLs
- **Changelog automatique** depuis le dernier tag
- **Instructions d'utilisation** pour chaque artifact

### Exemple de Release

```markdown
# Release v0.1.0

## Coordinated Release Artifacts

- **Python package**: `todolist@0.1.0`
- **Docker image**: `ghcr.io/naqa92/todolist:0.1.0` (also available as `latest`)
- **Helm chart**: `oci://ghcr.io/naqa92/charts/todolist:0.1.0`

## Changes

- feat: add user authentication
- fix: resolve database connection issue
- docs: update deployment guide
```

### Bonnes Pratiques

#### **Commits Conventionnels**

```bash
feat: nouvelle fonctionnalité
fix: correction de bug
docs: mise à jour documentation
chore: tâches de maintenance
```

#### **Stratégie de Branches**

- **`main`** : Branche de production (releases automatiques)
- **Feature branches** : Développement (pas de release)

#### **Gestion des Versions**

- **Auto-incrémentation** : Idéal pour le développement continu
- **Versions manuelles** : Pour les releases majeures/mineures planifiées

### Dépannage

#### **Version non incrémentée**

```bash
# Vérifier la version actuelle
grep 'version = ' pyproject.toml

# Voir les tags existants
git tag -l "v*"

# Forcer une nouvelle version
sed -i 's/version = "0.1.0"/version = "0.1.1"/' pyproject.toml
```

#### **Release échouée**

```bash
# Vérifier les logs du workflow
gh run list --workflow=ci.yaml

# Voir les détails d'un run
gh run view [RUN_ID]
```

## ☸️ Déploiement Kubernetes

### Déploiement Local avec Kind

```bash
# Créer cluster et déployer
task cluster-create

# Avec base de données externe
DATABASE_URL="postgresql://..." task cluster-create
```

- kind.yaml : exposition des ports 80 et 443
- ingress-nginx : activation du hostPort pour les ports 80 et 443
- déploiement de l'app : namespace, secret, deployment, service et ingress

Application accessible sur : todolist.127.0.0.1.nip.io

> _nip.io fonctionne en redirigeant 127.0.0.1.nip.io vers 127.0.0.1_

### Chart Helm todolist

#### Structure de la chart todolist

```
charts/todolist/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

#### Utilisation

```bash
helm template ./charts/todolist # Render
helm install todolist ./charts/todolist -n demo --create-namespace # Installation
helm upgrade todolist ./charts/todolist -n demo # Mise à jour
```

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.13+
- Docker
- (Optionnel) kubectl + kind pour Kubernetes

### Développement Local

```bash
# Cloner le projet
git clone https://github.com/naqa92/portfolio-ultime.git
cd portfolio-ultime

# Setup environnement Python
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt

# Lancer l'application
cd app
python app.py

# Accéder à l'application
open http://localhost:5000
```

### Tests de Développement

```bash
# Installation dépendances de test
pip install -r tests/requirements-dev.txt

# Tests unitaires
cd tests && pytest units.py -v

# Tests avec coverage
pytest units.py --cov=../app --cov-report=html
```

## 🔧 Configuration

### Variables d'Environnement

- `DATABASE_URL` : URL de connexion base de données
  - Dev : `sqlite:///todos.db` (défaut)
  - Prod : `postgresql://user:pass@host:port/db`

### Healthcheck

- **Endpoints** : `/health`
- **Réponse** : JSON
- **Utilisation** : Docker, Kubernetes, monitoring

| Paramètre             | Readiness Probe (Vérification de disponibilité)                                                   | Liveness Probe (Vérification de santé)                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `initialDelaySeconds` | Attend 5 secondes avant de commencer à vérifier si le conteneur est prêt à recevoir du trafic.    | Attend 30 secondes avant de commencer à vérifier si le conteneur est en vie.                      |
| `timeoutSeconds`      | La vérification doit se terminer en 5 secondes maximum, sinon elle est considérée comme un échec. | La vérification doit se terminer en 5 secondes maximum, sinon elle est considérée comme un échec. |

## 🛠️ Outils de Développement

### Devbox

Configuration dans `devbox-ci.json` pour :

- Installation de packages pour CI (Kind, kubectl, Helm et task)
- Exécution des scripts de test automatisés via Devbox pour CI

### Task Runner

`Taskfile.yaml` pour automatiser :

- Création cluster Kubernetes
- Déploiement application
- Gestion des dépendances

## Roadmap

- Branch Protection : Blocage des push directs sur main (Review MR nécessaire)

```yaml
on:
  pull_request:
    types:
      - opened
      - reopened
      - synchronize
      - closed # à séparer via pr-close.yaml
```

- Validation des données côté serveur plus stricte - Flask-WTF
- Gestion des migrations - Atlas
- Rate limiting - Protection contre les abus
- Monitoring - Métriques Prometheus/OpenTelemetry
- Improve frontend : Tailwind CSS, Alpine JS
- Démarrage Rapide : A revoir (simplifier)

---

> **Note** : Ce projet respecte le cahier des charges incluant dockerisation multi-stage, tests complets, pipeline CI/CD, et déploiement Kubernetes minimal.
