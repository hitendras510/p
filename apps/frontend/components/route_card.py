<<<<<<< HEAD
import streamlit as st

def render_route_card(route_data: dict, is_best_route: bool = False):
    """
    Renders a premium glassmorphic route card using custom HTML/CSS.
    """
    path = route_data.get("path", [])
    distance = route_data.get("distance", 0)
    traffic = route_data.get("traffic", 0)
    score = route_data.get("score", route_data.get("eco_score", "N/A"))
    fuel = route_data.get("fuel", "N/A")
    
    # Build path string
    path_str = " → ".join(path) if path else "Unknown"
    
    # Traffic level badge
    if traffic <= 3:
        traffic_label = "Low"
        traffic_class = "green"
        traffic_icon = "🟢"
    elif traffic <= 6:
        traffic_label = "Medium"
        traffic_class = "amber"
        traffic_icon = "🟡"
    else:
        traffic_label = "High"
        traffic_class = "red"
        traffic_icon = "🔴"
    
    # Score formatting
    if isinstance(score, (int, float)):
        score_display = f"{score:.2f}"
    else:
        score_display = str(score)

    if is_best_route:
        card_html = f"""
        <div class="best-route-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
                <span style="font-size: 1.4rem;">🏆</span>
                <span style="font-weight: 700; color: #34d399; font-size: 1rem;">EcoNav Recommended Route</span>
            </div>
            <div style="margin-bottom: 14px;">
                <span class="stat-pill green">📏 {distance} km</span>
                <span class="stat-pill {traffic_class}">{traffic_icon} Traffic: {traffic_label}</span>
                <span class="stat-pill blue">⚡ Score: {score_display}</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem;">
                <strong style="color: #f1f5f9;">Path:</strong> {path_str}
            </div>
        </div>
        """
    else:
        card_html = f"""
        <div class="alt-route-card">
            <div style="margin-bottom: 12px;">
                <span class="stat-pill">📏 {distance} km</span>
                <span class="stat-pill {traffic_class}">{traffic_icon} Traffic: {traffic_label}</span>
                <span class="stat-pill">⚡ Score: {score_display}</span>
            </div>
            <div style="color: #64748b; font-size: 0.85rem;">
                <strong style="color: #94a3b8;">Path:</strong> {path_str}
            </div>
        </div>
        """
    
    st.markdown(card_html, unsafe_allow_html=True)
=======
from __future__ import annotations

import streamlit as st

from apps.frontend.utils.formatters import parse_improvement_percent, route_to_string


def render_route_card(result: dict) -> None:
    improvement_pct = parse_improvement_percent(result.get("improvement", "N/A"))

    st.subheader("🌿 Recommended Eco Route")
    st.success(route_to_string(result["route"]))

    baseline_exposure = float(result.get("shortest_exposure", 0.0))
    eco_exposure = float(result.get("total_pollution", 0.0))
    exposure_delta = baseline_exposure - eco_exposure

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Distance", f"{float(result['total_distance']):.1f} km")
    col2.metric("Eco Exposure", f"{eco_exposure:.1f}")
    col3.metric("Baseline Exposure", f"{baseline_exposure:.1f}")
    col4.metric("Saved", f"{exposure_delta:.1f}")

    if improvement_pct is not None:
        progress_value = max(min(improvement_pct / 100, 1.0), 0.0)
        st.progress(progress_value, text=f"{improvement_pct:.2f}% cleaner")
    else:
        st.info("Improvement data not available for this route.")

    with st.expander("🔍 Compare with shortest route"):
        st.write("**Eco route:**", route_to_string(result["route"]))
        st.write("**Shortest path:**", route_to_string(result["shortest_route"]))
        st.write("**Improvement:**", result["improvement"])
>>>>>>> 8c3d578ab632eedee7d285f7a1cce0c2f1edc61d
