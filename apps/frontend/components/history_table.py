from __future__ import annotations

import streamlit as st

from apps.frontend.utils.formatters import compute_route_summary


def render_history_table(history: list[dict]) -> None:
    st.subheader("🕘 Recent Searches")
    if not history:
        st.info("No searches yet. Run your first route query.")
        return

    summary = compute_route_summary(history)
    left, right = st.columns(2)
    left.metric("Queries", int(summary["total_queries"]))
    right.metric("Avg Improvement", f"{float(summary['avg_improvement']):.2f}%")

    st.dataframe(history, use_container_width=True, hide_index=True)
