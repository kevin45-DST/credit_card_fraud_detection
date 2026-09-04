# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from typing import Any

from config.config_manager import ConfigManager
from src.agentic.llm.llm_backend import LLMBackend
from src.utils.imports_utils import ImportsUtils


class LLMManager:
    """
    Gestionnaire de LLM indépendant
    de l'implémentation utilisée.
    """

    @classmethod
    def create(
        cls,
    ) -> "LLMManager":
        """
        Crée un gestionnaire de LLM configuré.

        Returns
        -------
        LLMManager
            Gestionnaire de LLM configuré.
        """

        llm_config = ConfigManager(
            "config/mappings/llm.yaml"
        )

        project_config = ConfigManager(
            "config/project.yaml"
        )

        llm_type = project_config.get("llm.backend")

        backend_module = llm_config.get(
            f"{llm_type}.module"
        )

        backend_class_name = llm_config.get(
            f"{llm_type}.class"
        )

        backend_class = ImportsUtils.get_class(
            backend_module,
            backend_class_name,
        )

        backend = backend_class()

        return cls(
            backend=backend,
        )

    def __init__(
        self,
        backend: LLMBackend,
    ) -> None:
        """
        Initialise le gestionnaire de LLM.

        Parameters
        ----------
        backend :
            Implémentation du LLM utilisée.
        """

        self.backend = backend

    def start(
        self,
        context: str,
    ) -> None:
        """
        Initialise le contexte du LLM.

        Parameters
        ----------
        context :
            Identifiant du contexte à charger.
        """

        self.backend.initialize(context)

    def run(
        self,
        data: dict[str, Any],
    ) -> str:
        """
        Exécute une requête auprès du LLM.

        Parameters
        ----------
        data :
            Données nécessaires à l'exécution.

        Returns
        -------
        str
            Réponse générée par le LLM.
        """

        return self.backend.run(data)