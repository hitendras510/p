from __future__ import annotations

import streamlit as st
from requests import RequestException

from apps.frontend.services.api_client import fetch_health


def render_status_panel(api_url: str) -> None:
    st.subheader("🩺 API Diagnostics")
    st.caption("Check backend health and verify API connectivity.")

    if st.button("Check API health", use_container_width=True):
        try:
            payload = fetch_health(api_url)
            st.success("Backend is reachable")
            st.json(payload)
        except RequestException as exc:
            st.error(f"Health check failed: {exc}")
