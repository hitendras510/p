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
from components.route_card import render_route_card, CITY_NODES, route_to_string
from components.map_view import render_map_view
from components.ai_engine import render_ai_engine
from services.api_client import fetch_eco_route, check_backend_health

# ===== Hero Banner =====
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌿 EcoNav AI</h1>
        <p>AI-powered environmental decision intelligence for low-exposure route optimization. 
           Not just faster routes — smarter, healthier decisions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
    st.markdown(
        """
        <div class="glass-card" style="padding: 16px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">Quick Stats</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #94a3b8; font-size: 0.85rem;">Cities</span>
                <span style="color: #f1f5f9; font-weight: 600;">6</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #94a3b8; font-size: 0.85rem;">Model</span>
                <span style="color: #34d399; font-weight: 600;">Eco Scorer</span>
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

    # City reference
    st.markdown(
        '<div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase; '
        'letter-spacing: 0.05em; margin-bottom: 8px;">City Nodes</div>',
        unsafe_allow_html=True,
    )
    for node, city in CITY_NODES.items():
        st.markdown(
            f'<div style="color: #94a3b8; font-size: 0.82rem; margin-bottom: 4px;">'
            f'<strong style="color: #34d399;">{node}</strong> — {city}</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<div style="color: #475569; font-size: 0.7rem; text-align: center; margin-top: 16px;">'
        'Built with FastAPI + Streamlit + RL Agent<br>'
        '© 2026 EcoNav AI'
        '</div>',
        unsafe_allow_html=True,
    )


# ===== Main Tabs =====
tab_router, tab_ai = st.tabs(["🗺️  Eco-Router", "⚙️  AI Engine"])


# ──────────────────────────────────────────────
# TAB 1 — ECO-ROUTER
# ──────────────────────────────────────────────
with tab_router:
    st.markdown('<div class="section-header">🗺️ Find the Healthiest Route</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color: #94a3b8; margin-bottom: 20px;">'
        'Select a start and destination city. The RL agent will find the route '
        'with the lowest pollution exposure and compare it against the shortest path.'
        '</p>',
        unsafe_allow_html=True,
    )

    # City selection
    node_options = list(CITY_NODES.keys())
    city_labels = [f"{CITY_NODES[n]} ({n})" for n in node_options]
    
    col_src, col_dst = st.columns(2)
    with col_src:
        start_idx = st.selectbox("📍 Start City", range(len(node_options)),
                                 format_func=lambda i: city_labels[i], index=0, key="route_start")
    with col_dst:
        end_idx = st.selectbox("📍 Destination City", range(len(node_options)),
                               format_func=lambda i: city_labels[i], index=len(node_options) - 1, key="route_end")

    start_node = node_options[start_idx]
    end_node = node_options[end_idx]

    st.markdown("<br>", unsafe_allow_html=True)

    find_clicked = st.button("🔍  Find Eco-Route", key="btn_find_route", use_container_width=True)

    if find_clicked:
        if start_node == end_node:
            st.warning("Start and destination cannot be the same city.")
        else:
            with st.spinner("RL agent exploring routes & computing exposure scores…"):
                data = fetch_eco_route(start_node, end_node)

            if data is None:
                st.error("No data returned. Check backend logs.")
            else:
                # Store in session state for history
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.insert(0, {
                    "From": CITY_NODES[start_node],
                    "To": CITY_NODES[end_node],
                    "Eco Route": route_to_string(data["route"]),
                    "Improvement": data.get("improvement", "N/A"),
                })
                st.session_state.history = st.session_state.history[:5]

                st.markdown("<br>", unsafe_allow_html=True)

                # Layout: left = map, right = card
                col_map, col_card = st.columns([1.3, 1])

                with col_card:
                    st.markdown('<div class="section-header">🏆 Route Analysis</div>', unsafe_allow_html=True)
                    render_route_card(data)

                with col_map:
                    render_map_view(data)

    # Show recent search history
    if "history" in st.session_state and st.session_state.history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📋 Recent Searches</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.history, use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────
# TAB 2 — AI ENGINE
# ──────────────────────────────────────────────
with tab_ai:
    render_ai_engine()
