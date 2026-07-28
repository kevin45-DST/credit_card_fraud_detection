from typing import Any

import mlflow

from ..tracking_backend import TrackingBackend


class MLFlowBackend(TrackingBackend):
    """
    Implémentation du tracking utilisant MLflow.

    Cette classe adapte l'API MLflow au contrat défini
    par TrackingBackend.

    Le reste du framework ne connaît pas MLflow.
    """

    def __init__(
        self,
        experiment_name: str,
    ) -> None:

        mlflow.set_experiment(
            experiment_name
        )


    def start_run(
        self,
        run_name: str,
    ) -> None:

        mlflow.start_run(
            run_name=run_name
        )


    def log_params(
        self,
        params: dict[str, Any],
    ) -> None:

        mlflow.log_params(
            params
        )


    def log_metrics(
        self,
        metrics: dict[str, float],
    ) -> None:

        mlflow.log_metrics(
            metrics
        )


    def log_artifact(
        self,
        path: str,
    ) -> None:

        mlflow.log_artifact(
            path
        )


    def end_run(
        self,
    ) -> None:

        mlflow.end_run()