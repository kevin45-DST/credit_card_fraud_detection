# HephAIstOS

HephAIstOS (Heuristic & Pipeline Artificial Intelligence Orchestration System) est un framework modulaire conçu pour structurer, standardiser et exécuter les pipelines de Machine Learning.

## 🎯 Philosophie du Projet & Abstraction Strict

La force d'HephAIstOS réside dans son **indépendance technologique totale**. Le framework applique un découplage strict (SOLID) entre l'orchestration des pipelines de données et les outils ou librairies utilisés en tâche de fond.

### 🧱 Le modèle Managers / Backends
Le code métier manipule exclusivement des interfaces génériques :
*   **Les Managers** (ex: `TrainingManager`, `ModelPersistenceManager`) pilotent le flux logique et théorique sans jamais savoir quelle librairie est importée.
*   **Les Backends / Implémentations** (ex: `ScikitLearnBackend`, `XGBoostBackend`, `MLflowBackend`) encapsulent la complexité et la syntaxe propre à chaque outil tiers.

### 🛡️ Le principe du Verrou Fail-Fast
Pour préserver la pureté de cette abstraction, les classes mères ne possèdent aucune connaissance des contraintes techniques de leurs enfants. Lorsqu'une technologie concrète impose une compatibilité exclusive avec une autre, **ce verrou de sécurité est implémenté directement au sein du constructeur (`__init__`) de la classe concrète**. Si une mauvaise association est déclarée dans la configuration, le framework lève immédiatement une exception explicite au démarrage, protégeant l'intégrité de l'exécution avant le lancement des calculs.

---

## ⚙️ Centralisation de la Configuration

Le framework est entièrement déclaratif. L'utilisateur n'instancie jamais de classe technique dans ses scripts d'entraînement. Tout est centralisé et injecté dynamiquement :
1.  L'utilisateur choisit ses briques dans le fichier `config/implementations.yaml` (ex: `backend: mlflow`).
2.  Le `config_manager.py` consulte les dictionnaires de correspondance situés dans `config/mappings/`.
3.  Les classes Python concrètes sont chargées et injectées à la volée dans les composants du framework.

---

## 📁 Architecture du Framework

L'arborescence des fichiers met en évidence la séparation étanche entre l'orchestration, les outils de la boîte à outils et le système :

*   **`config/`** : Centralisation de la configuration (fichiers YAML), des chemins (`paths.yaml`) et logique d'injection des dépendances (`config_manager.py`).
*   **`src/ml_pipeline/`** : Orchestrateurs de haut niveau (Search, Training, Tracking). Ces pipelines décrivent les "recettes" d'exécution et manipulent uniquement des abstractions.
*   **`src/ml_toolbox/`** : La boîte à outils modulaire.
    *   `data_science/` : Stratégies de recherche d'hyperparamètres et prétraitement (Scaling, Encoding, Balancing).
    *   `mlops/` : Gestion du cycle de vie et tracking des expériences (ex: `MLflowBackend`).
    *   `transversal/` : Composants horizontaux réutilisables (Persistance avec Joblib, Évaluation, Reporting).
    *   `helpers/` : Applications et outils spécifiques à destination de l'utilisateur (ex: l'interface interactive `decision_helper`).
*   **`src/utils/`** : Utilitaires techniques système agnostiques au Machine Learning (gestion des dates, IDs uniques, imports dynamiques).
    *   `helpers/` : Modules de maintenance et de résilience système autonome (scripts de `recovery` en cas de panne).
*   **`scripts/`** : Scripts système d'initialisation automatique de l'environnement virtuel (`.sh`, `.bat`, `.ps1`).
*   **`tests/`** : Tests unitaires et d'intégration garantissant la non-régression du framework.

---

## 🚀 Démarrage Rapide

1.  **Initialiser l'environnement** en exécutant le script adapté à votre système à la racine du projet (ex: `sh scripts/init_env.sh` ou `./scripts/init_env.ps1`).
2.  **Activer l'environnement virtuel** (`source .venv/bin/activate`).
3.  **Installer les dépendances** via `pip install -r requirements.txt`.
4.  **Définir vos briques technologiques** dans `config/implementations.yaml`.
5.  **Exécuter le point d'entrée principal** :
    ```bash
    python main.py
    ```
