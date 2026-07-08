import streamlit as st
import pandas as pd

from pathlib import Path


class MetricTable:

    def __init__(
        self,
        metrics: pd.DataFrame,
        report_path: Path,
    ) -> None:

        self.metrics = metrics
        self.report_path = report_path

    def show(self):

        for _, row in self.metrics.iterrows():

            c1, c2, c3 = st.columns(
                [7,1,1]
            )

            with c1:

                st.write(
                    row.to_frame().T
                )

            with c2:

                if st.button(
                    "📊",
                    key=f"cm_{row['label']}",
                ):

                    st.session_state["selected_model"] = row["label"]
                    st.session_state["selected_view"] = "confusion"

            with c3:

                if st.button(
                    "🧠",
                    key=f"fi_{row['label']}",
                ):

                    st.session_state["selected_model"] = row["label"]
                    st.session_state["selected_view"] = "importance"