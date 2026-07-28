from pathlib import Path
import json
import sys

sys.path.append(
    str(Path(__file__).resolve().parents[4])
)

from config.config_manager import ConfigManager


class ExperimentRecovery:
    """
    Permet de reconstruire le registre global des expériences
    à partir des registres locaux présents dans chaque dossier
    d'expérience.
    """

    def __init__(
        self,
        experiments_path: Path,
        global_registry_path: Path,
    ) -> None:
        """
        Initialise le composant de reconstruction des expériences.

        Parameters
        ----------
        experiments_path : Path
            Dossier contenant les différentes expériences.

        global_registry_path : Path
            Chemin du fichier 'experiments_registry.json' à reconstruire.
        """

        self.experiments_path = experiments_path
        self.global_registry_path = global_registry_path

    def recover(self) -> list[dict]:
        """
        Parcourt les dossiers d'expériences et récupère les informations
        contenues dans chaque fichier 'experiment_registry.json'.

        Returns
        -------
        list[dict]
            Liste des expériences récupérées.
        """

        experiments = []

        if not self.experiments_path.exists():
            return experiments

        for experiment_dir in self.experiments_path.iterdir():

            if not experiment_dir.is_dir():
                continue

            if not experiment_dir.name.startswith(
                "experiment_"
            ):
                continue

            registry_path = (
                experiment_dir
                / "experiment_registry.json"
            )

            if not registry_path.exists():
                continue

            experiment = self._load_registry(
                registry_path
            )

            if experiment:
                experiments.append(experiment)

        return experiments

    def rebuild_global_registry(
        self,
        experiments: list[dict],
    ) -> None:
        """
        Reconstruit le fichier 'experiments_registry.json'
        à partir de la liste des expériences récupérées.

        Parameters
        ----------
        experiments : list[dict]
            Liste des expériences à enregistrer dans le registre global.
        """

        registry = {
            "experiments": experiments
        }

        self.global_registry_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.global_registry_path / "experiments_registry.json",
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                registry,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def recover_and_rebuild(self) -> list[dict]:
        """
        Reconstruit le registre global des expériences.

        Cette méthode récupère les informations contenues dans les
        registres locaux de chaque expérience puis génère un nouveau
        fichier 'experiments_registry.json'.

        Returns
        -------
        list[dict]
            Liste des expériences récupérées.
        """

        experiments = self.recover()

        self.rebuild_global_registry(
            experiments
        )

        return experiments

    @staticmethod
    def _load_registry(
        registry_path: Path,
    ) -> dict | None:
        """
        Charge le registre local d'une expérience.

        Parameters
        ----------
        registry_path : Path
            Chemin vers le fichier 'experiment_registry.json'.

        Returns
        -------
        dict | None
            Contenu du registre si le fichier est valide,
            sinon None.
        """

        try:
            with open(
                registry_path,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except json.JSONDecodeError:
            return None
        
def main() -> None:
    
    config = ConfigManager(
            "config/paths.yaml"
        )

    training_path = Path(config.get("project.root")) / config.get("reports.root") / config.get("reports.training")

    recovery = ExperimentRecovery(
        experiments_path = training_path,
        global_registry_path = training_path,
    )

    experiments = recovery.recover_and_rebuild()

    print(
        f"{len(experiments)} experiments_registry restauré."
    )


if __name__ == "__main__":
    main()