from typing import Any

from .tracking_backend import TrackingBackend


class TrackingManager:
    """
    Gestionnaire de tracking indépendant du backend utilisé.

    Cette classe fait le lien entre les pipelines du framework
    et le système de tracking choisi.

    Elle masque l'implémentation technique du backend.

    Exemple :
        TrackingManager(MLFlowTracking())

    Le pipeline manipule uniquement ce composant et ne dépend
    jamais directement de MLflow.
    """

    def __init__(
        self,
        backend: TrackingBackend,
    ) -> None:

        self.backend = backend


    def track_training(
        self,
        run_name: str,
        params: dict[str, Any],
        metrics: dict[str, float],
        artifact_path: str | None = None,
    ) -> None:
        """
        Enregistre une expérience d'entraînement.

        Parameters
        ----------
        run_name :
            Nom de l'expérience.

        params :
            Paramètres utilisés lors de l'entraînement.

        metrics :
            Métriques obtenues.

        artifact_path :
            Chemin optionnel vers un artefact
            (modèle, rapport...).
        """

        self.backend.start_run(
            run_name
        )

        self.backend.log_params(
            params
        )

        self.backend.log_metrics(
            metrics
        )

        if artifact_path:
            self.backend.log_artifact(
                artifact_path
            )

        self.backend.end_run()