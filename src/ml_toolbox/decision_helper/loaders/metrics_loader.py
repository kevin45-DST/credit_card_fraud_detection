from pathlib import Path

import pandas as pd


class MetricsLoader:

    def __init__(
        self,
        report_path: Path,
    ) -> None:

        self.report_path = report_path

    def load(self) -> pd.DataFrame:

        return pd.read_csv(
            self.report_path / "report.csv"
        )