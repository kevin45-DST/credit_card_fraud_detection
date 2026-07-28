from src.ml_toolbox.mlops.tracking.implementations.mlflow_Backend import MLFlowBackend
from src.ml_toolbox.mlops.tracking.tracking_manager import TrackingManager


class TrackingPipeline:


    def __init__(self, experiment_name: str):
        
        tracking = TrackingManager(
            MLFlowBackend(
                experiment_name=experiment_name
            )
        )

tracking.track_training(
    run_name="RandomForest_v1",
    params={
        "n_estimators":100
    },
    metrics={
        "f1":0.92
    },
    artifact_path="models/model.joblib"
)