# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from pathlib import Path
from typing import Any

from src.agentic.llm.llm_manager import LLMManager


class CodeAnalysis:
    """
    Analyse un ensemble de fichiers source à l'aide d'un LLM.
    """
    
    SUPPORTED_EXTENSIONS = {
        ".py",
        ".yaml",
        ".yml",
    }
    
    def __init__(
        self,
    ) -> None:
        """
        Initialise l'analyseur de code.
        """

        self.llm_manager = LLMManager.create()

    def start(
        self,
    ) -> None:
        """
        Initialise le contexte LLM utilisé pour l'analyse de code.
        """

        self.llm_manager.start("code_analysis")

    def analyse(
        self,
        paths: list[str | Path],
        report_path: str | Path,
    ) -> None:
        """
        Analyse récursivement les fichiers présents dans plusieurs dossiers.

        Parameters
        ----------
        paths :
            Liste des dossiers ou fichiers à analyser.

        report_path :
            Chemin du rapport à générer.
        """

        source_files = self._collect_source_files(paths)

        result = self.llm_manager.run(
            {
                "source_files": source_files,
            }
        )

        report_path = Path(report_path)

        report_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path.write_text(
            result,
            encoding="utf-8",
        )

    def _collect_source_files(
        self,
        paths: list[str | Path],
    ) -> list[dict[str, Any]]:
        """
        Collecte récursivement les fichiers à analyser.

        Parameters
        ----------
        paths :
            Liste des dossiers ou fichiers à parcourir.

        Returns
        -------
        list[dict[str, Any]]
            Fichiers collectés avec leur chemin et leur contenu.
        """

        source_files = []

        for path_value in paths:
            path = Path(path_value)

            if path.is_file():
                if path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    source_files.append(
                        self._read_source_file(path)
                    )
                continue

            if path.is_dir():
                for file_path in path.rglob("*"):
                    if (file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS):
                        source_files.append(
                            self._read_source_file(file_path)
                        )

        return source_files

    def _read_source_file(
        self,
        path: Path,
    ) -> dict[str, Any]:
        """
        Lit un fichier à analyser.

        Parameters
        ----------
        path :
            Chemin du fichier.

        Returns
        -------
        dict[str, Any]
            Chemin et contenu du fichier.
        """

        return {
            "file_path": str(path),
            "source_code": path.read_text(
                encoding="utf-8",
            ),
        }