from pathlib import Path

import numpy as np
from pandas import Series
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from config.config_manager import ConfigManager
from src.ml_toolbox.dataset.dataset import Dataset
from src.ml_toolbox.preprocessing.scaling.basic import BasicScaling
from src.ml_training.training_pipeline import TrainingPipeline
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
    y = Series(df["Class"])
    
    X_sample, y_sample = BasicBalancing.smote_tomek(X, y)
    
    ds = Dataset("dataset_test", X_sample, y_sample)
    
    ds.x_train, ds.x_test, ds.y_train, ds.y_test, scaler = BasicScaling.standard(ds.x_train, ds.x_test, ds.y_train, ds.y_test)

    return ds


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
        dataset=dataset,
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
        dataset=dataset,
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