# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import json
from datetime import datetime
from typing import Any
from urllib.request import Request, urlopen

from config.config_manager import ConfigManager
from src.ml_toolbox.transversal.logs.log_storage.log_storage_backend import LogStorageBackend


class ElasticSearchBackend(LogStorageBackend):
    """
    Backend de stockage des logs dans kibana elasticsearch.

    Les logs sont envoyés à elasticsearch via son API HTTP.
    Le backend ne réalise aucun filtrage des logs.
    """

    def __init__(
        self,
        labels: dict[str, str] | None = None,
    ) -> None:
        """
        Initialise le backend elasticsearch.

        Args:
            url: URL de l'API push de elasticsearch.
            labels: Labels statiques associés aux logs.
        """
        project_config = ConfigManager("config/project.yaml")
        
        self._url = project_config.get("logs.storage.url")
        
        self._push_url = f"{self._url}/pipeline-logs/_doc"
        self._labels = labels or {}

    def store(self, log: dict[str, Any]) -> None:
        """
        Envoie un log à elasticsearch.

        Args:
            log: Log à stocker.
        """
        print("Store backend")
        timestamp = self._get_timestamp(log)
        payload = self._build_payload(log, timestamp)
        print(f"{self._push_url = }, {payload = }")
        request = Request(
            self._push_url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            #response.read()
            print(f"elasticsearch HTTP status: {response.status}")
            print(f"elasticsearch response: {response.read().decode('utf-8')}")

    def close(self) -> None:
        """Ferme le backend elasticsearch."""

    def _build_payload(
        self,
        log: dict[str, Any],
        timestamp: int,
    ) -> dict[str, Any]:
        """
        Construit le payload attendu par l'API Elasticsearch.
        Fusionne les labels statiques globaux et normalise la date.
        """
        # On crée une copie pour ne pas altérer le dictionnaire d'origine
        payload = log.copy()
        
        # Injection des labels globaux s'ils existent (ex: env, app_name)
        if self._labels:
            payload["labels"] = self._labels

        # Elasticsearch gère nativement le format ISO 8601 présent dans vos logs.
        # Si absent, on génère une date au format ISO conforme.
        if "timestamp" not in payload:
            payload["timestamp"] = timestamp

        return payload

    @staticmethod
    def _get_timestamp(log: dict[str, Any]) -> int:
        """
        Convertit le timestamp du log en nanosecondes UTC.

        Args:
            log: Log contenant le timestamp ISO 8601.

        Returns:
            Timestamp Unix exprimé en nanosecondes.
        """
        timestamp = log.get("timestamp")

        if not timestamp:
            return int(datetime.now().timestamp() * 1_000_000_000)

        parsed_timestamp = datetime.fromisoformat(timestamp)

        return int(parsed_timestamp.timestamp() * 1_000_000_000)