# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import json
from typing import Any
from urllib.request import Request, urlopen

from config.config_manager import ConfigManager
from src.agentic.llm.llm_backend import LLMBackend


class OllamaBackend(LLMBackend):
    """
    Backend LLM utilisant Ollama.

    Le backend charge le contexte demandé depuis la configuration,
    transmet les données au modèle et retourne la réponse générée.
    """

    def __init__(self) -> None:
        """Initialise la configuration du backend Ollama."""
        project_config = ConfigManager("config/project.yaml")

        self._url = project_config.get("llm.url")
        self._model = project_config.get("llm.model")
        self._prompt: str | None = None

    def initialize(self, context: str) -> None:
        """
        Initialise le contexte utilisé par le LLM.

        Args:
            context: Identifiant du contexte à charger.
        """
        prompt_config = ConfigManager(f"config/prompts/{context}.yaml")
        self._prompt = prompt_config.get("prompt")

    def run(self, data: dict[str, Any]) -> str:
        """
        Exécute une requête auprès du modèle.

        Args:
            data: Données à transmettre au LLM.

        Returns:
            Réponse générée par le modèle.

        Raises:
            RuntimeError: Si le backend n'a pas été initialisé.
        """
        if self._prompt is None:
            raise RuntimeError(
                "Le backend LLM doit être initialisé avant son utilisation."
            )

        payload = {
            "model": self._model,
            "messages": [
                {
                    "role": "system",
                    "content": self._prompt,
                },
                {
                    "role": "user",
                    "content": json.dumps(data, ensure_ascii=False),
                },
            ],
            "stream": False,
        }

        request = Request(
            f"{self._url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["message"]["content"]