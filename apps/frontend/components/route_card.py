import streamlit as st


# City node mapping — matches the graph defined in route_service.py
CITY_NODES = {
    "A": "Delhi",
    "B": "Jaipur",
    "C": "Agra",
    "D": "Varanasi",
    "E": "Lucknow",
    "F": "Kolkata",
}

NODE_COORDS = {
    "A": [28.6139, 77.2090],
    "B": [26.9124, 75.7873],
    "C": [27.1767, 78.0081],
    "D": [25.3176, 82.9739],
    "E": [26.8467, 80.9462],
    "F": [22.5726, 88.3639],
}


def node_label(node: str) -> str:
    """Convert node ID to 'City (ID)' format."""
    city = CITY_NODES.get(node, node)
    return f"{city} ({node})" if city != node else node


def route_to_string(path: list) -> str:
    """Convert a path list like ['A','B','F'] to 'Delhi → Jaipur → Kolkata'."""
    return " → ".join(CITY_NODES.get(n, n) for n in path)


def render_route_card(result: dict) -> None:
    """
    Renders a premium card for the eco-route result from the backend.
    Expects keys: route, total_distance, total_pollution, shortest_route,
                  shortest_exposure, improvement
    """
    eco_path = result.get("route", [])
    shortest_path = result.get("shortest_route", [])
    eco_exposure = float(result.get("total_pollution", 0))
    baseline_exposure = float(result.get("shortest_exposure", 0))
    distance = float(result.get("total_distance", 0))
    improvement = result.get("improvement", "N/A")
    exposure_saved = baseline_exposure - eco_exposure

    # Parse improvement percentage
    imp_pct = None
    if improvement and improvement != "N/A":
        try:
            imp_pct = float(improvement.split("%")[0].strip())
        except ValueError:
            imp_pct = None

    # --- Best Route Card ---
    card_html = f"""
    <div class="best-route-card">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
            <span style="font-size: 1.4rem;">🏆</span>
            <span style="font-weight: 700; color: #34d399; font-size: 1rem;">EcoNav Recommended Route</span>
        </div>
        <div style="margin-bottom: 14px;">
            <span class="stat-pill green">📏 {distance:.1f} km</span>
            <span class="stat-pill blue">🌫️ Exposure: {eco_exposure:.1f}</span>
            <span class="stat-pill green">💨 Saved: {exposure_saved:.1f}</span>
        </div>
        <div style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 8px;">
            <strong style="color: #f1f5f9;">Eco Path:</strong> {route_to_string(eco_path)}
        </div>
        <div style="color: #64748b; font-size: 0.82rem;">
            <strong style="color: #94a3b8;">Shortest Path:</strong> {route_to_string(shortest_path)}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # Progress bar for improvement
    if imp_pct is not None and imp_pct > 0:
        progress = max(min(imp_pct / 100, 1.0), 0.0)
        st.progress(progress, text=f"🌿 {imp_pct:.1f}% cleaner than shortest route")
    elif imp_pct == 0:
        st.info("ℹ️ Eco route matches the shortest route for this pair.")
    else:
        st.info("ℹ️ Improvement data not available.")

    # Comparison expander
    with st.expander("🔍 Detailed Route Comparison"):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Eco Distance", f"{distance:.1f} km")
        col2.metric("Eco Exposure", f"{eco_exposure:.1f}")
        col3.metric("Baseline Exposure", f"{baseline_exposure:.1f}")
        col4.metric("Exposure Saved", f"{exposure_saved:.1f}")
        st.markdown(f"**Improvement:** {improvement}")
