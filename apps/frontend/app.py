<<<<<<< HEAD
import streamlit as st

# ===== Page Config (must be first Streamlit call) =====
st.set_page_config(
    page_title="EcoNav AI — Intelligent Routing",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== Inject Premium Theme =====
from styles import inject_theme
inject_theme()

# ===== Imports =====
from components.route_card import render_route_card
from components.map_view import render_map_view
from components.environment_manager import render_environment_manager, get_place_names, build_routes_from_places
from components.ai_engine import render_ai_engine
from services.api_client import fetch_eco_routes, check_backend_health

# ===== Hero Banner =====
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌿 EcoNav AI</h1>
        <p>AI-powered environmental decision intelligence for low-exposure route optimization. 
           Not just faster routes — smarter, healthier decisions.</p>
=======
from __future__ import annotations

import streamlit as st
from requests import RequestException

from apps.frontend.components.map_view import render_map_view
from apps.frontend.components.route_card import render_route_card
from apps.frontend.services.api_client import DEFAULT_BASE_URL, fetch_eco_route
from apps.frontend.utils.formatters import route_to_string

st.set_page_config(page_title="EcoNav AI", page_icon="🌱", layout="wide")

st.markdown(
    """
    <style>
      .block-container {padding-top: 1.5rem;}
      .hero-card {
        padding: 1rem 1.2rem;
        border-radius: 1rem;
        background: linear-gradient(90deg, #d9f99d 0%, #bbf7d0 45%, #a7f3d0 100%);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
      <h2>🌱 EcoNav AI</h2>
      <p>Plan cleaner city routes with exposure-aware optimization.</p>
>>>>>>> 8c3d578ab632eedee7d285f7a1cce0c2f1edc61d
    </div>
    """,
    unsafe_allow_html=True,
)

<<<<<<< HEAD
# ===== Sidebar =====
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 24px;">
            <div style="font-size: 2.5rem; margin-bottom: 6px;">🌿</div>
            <div style="font-weight: 800; font-size: 1.3rem; 
                        background: linear-gradient(135deg, #10b981, #3b82f6);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                EcoNav AI
            </div>
            <div style="color: #64748b; font-size: 0.75rem; margin-top: 2px;">v1.0 — Intelligent Routing</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Backend health indicator
    is_online = check_backend_health()
    if is_online:
        st.markdown(
            '<div style="font-size: 0.82rem; color: #94a3b8;">'
            '<span class="status-dot online"></span> Backend: <strong style="color: #34d399;">Online</strong>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="font-size: 0.82rem; color: #94a3b8;">'
            '<span class="status-dot offline"></span> Backend: <strong style="color: #ef4444;">Offline</strong>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    # Quick stats
    places = get_place_names()
    st.markdown(
        f"""
        <div class="glass-card" style="padding: 16px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">Quick Stats</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #94a3b8; font-size: 0.85rem;">Places</span>
                <span style="color: #f1f5f9; font-weight: 600;">{len(places)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #94a3b8; font-size: 0.85rem;">Model</span>
                <span style="color: #34d399; font-weight: 600;">PyTorch MLP</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #94a3b8; font-size: 0.85rem;">Hot-Reload</span>
                <span style="color: #34d399; font-weight: 600;">Enabled</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div style="color: #475569; font-size: 0.7rem; text-align: center; margin-top: 16px;">'
        'Built with FastAPI + Streamlit + PyTorch<br>'
        '© 2026 EcoNav AI'
        '</div>',
        unsafe_allow_html=True,
    )


# ===== Main Tabs =====
tab_router, tab_env, tab_ai = st.tabs(["🗺️  Eco-Router", "🌍  Environment Manager", "⚙️  AI Engine"])


# ──────────────────────────────────────────────
# TAB 1 — ECO-ROUTER
# ──────────────────────────────────────────────
with tab_router:
    st.markdown('<div class="section-header">🗺️ Find the Healthiest Route</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color: #94a3b8; margin-bottom: 20px;">'
        'Type any real place names to let the AI find the route '
        'with the lowest pollution exposure. Intermediate waypoints are pulled from your Environment.'
        '</p>',
        unsafe_allow_html=True,
    )

    places = get_place_names()

    col_src, col_dst = st.columns(2)
    with col_src:
        source = st.text_input("📍 Source", value="", placeholder="e.g. Connaught Place, Delhi", key="route_source")
    with col_dst:
        destination = st.text_input("📍 Destination", value="", placeholder="e.g. India Gate, Delhi", key="route_dest")

    st.markdown("<br>", unsafe_allow_html=True)

    find_clicked = st.button("🔍  Find Eco-Route", key="btn_find_route", use_container_width=True)

    if find_clicked:
        if not source.strip() or not destination.strip():
            st.warning("Please enter both a source and a destination.")
        elif source.strip().lower() == destination.strip().lower():
            st.warning("Source and destination cannot be the same.")
        else:
            with st.spinner("Generating candidate routes & scoring with AI model…"):
                # Build routes from the user-defined places
                candidate_routes = build_routes_from_places(source, destination)
                data = fetch_eco_routes(candidate_routes)

                best_route = data.get("best_route")
                all_routes = data.get("all_routes", [])

            if not best_route and not all_routes:
                st.error("No routes were returned. Check backend logs.")
            else:
                st.markdown("<br>", unsafe_allow_html=True)

                # Layout: left = map, right = cards
                col_map, col_cards = st.columns([1.3, 1])

                with col_map:
                    render_map_view(all_routes, best_route)

                with col_cards:
                    if best_route:
                        st.markdown('<div class="section-header">🏆 Optimal Eco-Route</div>', unsafe_allow_html=True)
                        render_route_card(best_route, is_best_route=True)

                    alternatives = [r for r in all_routes if r.get("path") != (best_route or {}).get("path")]
                    if alternatives:
                        st.markdown('<div class="section-header">📋 Alternative Routes</div>', unsafe_allow_html=True)
                        for route in alternatives:
                            render_route_card(route, is_best_route=False)

                # Summary metrics row
                if all_routes:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="section-header">📊 Route Comparison Summary</div>', unsafe_allow_html=True)
                    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                    with mcol1:
                        st.metric("Routes Analyzed", len(all_routes))
                    with mcol2:
                        avg_dist = sum(r.get("distance", 0) for r in all_routes) / len(all_routes)
                        st.metric("Avg Distance", f"{avg_dist:.1f} km")
                    with mcol3:
                        avg_traffic = sum(r.get("traffic", 0) for r in all_routes) / len(all_routes)
                        st.metric("Avg Traffic", f"{avg_traffic:.1f}/10")
                    with mcol4:
                        if best_route:
                            st.metric("Best Score", f"{best_route.get('score', 'N/A')}")


# ──────────────────────────────────────────────
# TAB 2 — ENVIRONMENT MANAGER
# ──────────────────────────────────────────────
with tab_env:
    render_environment_manager()


# ──────────────────────────────────────────────
# TAB 3 — AI ENGINE
# ──────────────────────────────────────────────
with tab_ai:
    render_ai_engine()
=======
with st.sidebar:
    st.header("Settings")
    api_url = st.text_input("Backend API URL", value=DEFAULT_BASE_URL)
    preset = st.selectbox("Quick route preset", ["A → F", "A → E", "C → F"], index=0)

start_default, end_default = [x.strip() for x in preset.split("→")]

with st.form("eco_route_form"):
    col1, col2 = st.columns(2)
    start = col1.text_input("Start node", value=start_default)
    end = col2.text_input("Destination node", value=end_default)
    submitted = st.form_submit_button("Find Eco Route", use_container_width=True)

if "history" not in st.session_state:
    st.session_state.history = []

if submitted:
    if not start or not end:
        st.warning("Please provide both start and destination nodes.")
    else:
        try:
            data = fetch_eco_route(start, end, api_url)
            st.session_state.history.insert(
                0,
                {
                    "from": start.upper(),
                    "to": end.upper(),
                    "route": route_to_string(data["route"]),
                    "improvement": data["improvement"],
                },
            )
            st.session_state.history = st.session_state.history[:5]

            left, right = st.columns([1.2, 1])
            with left:
                render_route_card(data)
            with right:
                render_map_view(data["route"])
        except RequestException as exc:
            st.error(f"Failed to reach backend API: {exc}")
        except Exception as exc:  # noqa: BLE001
            st.error(f"Unexpected error: {exc}")

if st.session_state.history:
    st.markdown("### Recent Searches")
    st.dataframe(st.session_state.history, use_container_width=True, hide_index=True)
>>>>>>> 8c3d578ab632eedee7d285f7a1cce0c2f1edc61d
