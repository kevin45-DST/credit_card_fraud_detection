from pathlib import Path

import streamlit as st
import pandas as pd

from widgets.metric_table import MetricTable


class MetricsView:

    def __init__(
        self,
        metrics: pd.DataFrame,
        report_path: Path,
    ) -> None:

        self.metrics = metrics
        self.report_path = report_path

    def show(self) -> None:

        st.title("Decision Helper")

        MetricTable(
            self.metrics,
            self.report_path,
        ).show()