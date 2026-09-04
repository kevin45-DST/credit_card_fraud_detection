# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from abc import ABC, abstractmethod
from typing import Any


class LLMBackend(ABC):
    """
    Interface définissant le contrat d'un backend LLM.

    Un backend LLM est responsable de l'initialisation du contexte
    et de l'exécution des requêtes auprès du modèle.
    """

    @abstractmethod
    def initialize(self, context: str) -> None:
        """
        Initialise le LLM avec le contexte demandé.

        Args:
            context: Identifiant du contexte à utiliser.
        """
        pass

    @abstractmethod
    def run(self, data: dict[str, Any]) -> str:
        """
        Exécute une requête auprès du LLM.

        Args:
            data: Données nécessaires à l'exécution.

        Returns:
            Réponse générée par le LLM.
        """
        pass