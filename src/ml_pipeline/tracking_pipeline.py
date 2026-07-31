from asyncio import exceptions
import json
from pathlib import Path

import pandas as pd

from config.config_manager import ConfigManager
from src.ml_toolbox.mlops.tracking.tracking_manager import TrackingManager


class TrackingPipeline:


    def __init__(self):

        self.tracking_manager = TrackingManager.create()
        
    def get_runs_to_track(self):
        
        runs_to_track = []
        
        config = ConfigManager(
            "config/paths.yaml"
        )

        registry_path = (
            Path(config.get("project.root_folder")) 
            / config.get("reports.root_folder") 
            / config.get("reports.training") 
            / "runs_registry.json"
        )
        
        try:
            with open(
                registry_path,
                "r",
                encoding="utf-8",
            ) as file:

                runs: dict = json.load(file)

                for run in runs["runs"]:
                    if "tracking_status" not in run:
                        runs_to_track.append(
                            run["run_id"]
                        )
                        
            return runs_to_track
            
        except json.JSONDecodeError as e:
            raise e

    def run(self):
        
        config = ConfigManager(
            "config/paths.yaml"
        )
        
        # Recherche de la liste des runs à tracker
        runs_to_track = self.get_runs_to_track()
        
        # Initialisation de l'experience
        self.tracking_manager.initialize_experiment()
  
        for run_id in runs_to_track:
        
            try:
                # Démarrage du tracking de l'expérience
                self.tracking_manager.start_run(run_id)

                # Enregistrement des paramètres
                #self.tracking_manager.params(params)

                run_path = (
                    Path(config.get("project.root_folder")) 
                    / config.get("reports.root_folder") 
                    / config.get("reports.training") 
                    / run_id
                )
                
                report = pd.read_csv(run_path / "report.csv")
                
                metrics: dict[str, float] = {
                    str(key): float(value)
                    for key, value in (
                        report
                        .drop(columns=["model"])
                        .iloc[0]
                        .items()
                    )
                }

                # Enregistrement des métriques
                self.tracking_manager.metrics(metrics)

                # Enregistrement des artefacts
                self.tracking_manager.artifact(run_path / "artifacts")

            finally:
                # Fin du tracking
                self.tracking_manager.end_run()