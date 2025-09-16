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
