from pathlib import Path

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from config.config_manager import ConfigManager
from src.ml_training.training_pipeline import TrainingPipeline
from src.ml_training.dataset_manager import DatasetManager
from src.ml_training.search_pipeline import SearchPipeline
from src.ml_toolbox.preprocessing.balancing.basic import BasicBalancing

import pandas as pd


def build_datasets():
    """
    Exemple de construction des datasets.
    À remplacer par ton preprocessing réel.
    """

    df = pd.read_csv("data/raw/creditcard.csv")
    
    X = df.drop("Class", axis=1)
    y = df["Class"]
    
    X_sample, y_sample = BasicBalancing.smote_tomek(X, y)

    print(y_sample.value_counts())

    manager = DatasetManager()

    manager.add_dataset(
        name="raw_dataset",
        x=X_sample,
        y=y_sample,
        test_size=0.2,
        stratify=True,
    )

    return manager.get_datasets()


def build_models():
    """
    Définition des modèles à tester.
    """

    return {
        "RandomForestClassifier": RandomForestClassifier(class_weight="balanced"),
        "GradientBoostingClassifier": GradientBoostingClassifier()
    }


def build_param_grids():
    """
    Grilles d'hyperparamètres.
    """

    return {
        "RandomForestClassifier": {
            "n_estimators": [100, 200],
            "max_depth": [None, 10, 20],
        },
        "GradientBoostingClassifier": {
            "n_estimators": [100, 200],
            "learning_rate": [0.05, 0.1],
        },
    }

    
def search():
    
    config = ConfigManager(
            "config/paths.yaml"
        )
    report_path = config.get(
            "reports.search"
        )
    
    print("Starting training pipeline...")

    dataset = build_datasets()
    models = build_models()
    param_grids = build_param_grids()
    
    scorings = "f1_macro"

    pipeline = SearchPipeline(
        dataset=dataset[0],
        models=models,
        param_grids=param_grids,
        report_path=report_path,
        scorings=scorings,
        cv=5,
    )

    pipeline.run()

    print("Training finished.")
    
def train():
    
    config = ConfigManager(
            "config/paths.yaml"
        )

    report_path = config.get(
            "reports.training"
        )
    models_path = config.get("models.path")
    
    print("Starting training pipeline...")

    model_name = "RandomForestClassifier"
    model = RandomForestClassifier()
    params = {'max_depth': None, 'n_estimators': 200}
    
    dataset = build_datasets()

    pipeline = TrainingPipeline(
        dataset=dataset[0],
        model=model,
        model_name=model_name,
        params=params,
        report_path=report_path,
        candidate_path=models_path
    )

    pipeline.run()

    print("Training finished.")

def main():
    search()
    #train()

if __name__ == "__main__":
    main()