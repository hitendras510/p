<<<<<<< HEAD
import streamlit as st

def render_map_view(routes: list, best_route: dict = None):
    """
    Renders a professional Graphviz visualization of all available routes.
    The best route is highlighted in green, other paths are shown as dashed grey.
    """
    if not routes:
        st.info("No routes to display on the map.")
        return

    # Build directed graph DOT source
    lines = []
    lines.append("digraph Routes {")
    lines.append("  rankdir=LR;")
    lines.append("  bgcolor=\"transparent\";")
    lines.append("  pad=0.5;")
    lines.append("  nodesep=0.8;")
    lines.append("  ranksep=1.2;")
    # Node styling
    lines.append('  node [shape=box, style="rounded,filled", fontname="Inter", fontsize=11, '
                 'fillcolor="#1e293b", fontcolor="#e2e8f0", color="#334155", penwidth=1.5];')
    # Edge defaults
    lines.append('  edge [fontname="Inter", fontsize=9, fontcolor="#64748b"];')

    best_path_edges = set()
    if best_route and "path" in best_route:
        nodes = best_route["path"]
        for i in range(len(nodes) - 1):
            best_path_edges.add((nodes[i], nodes[i + 1]))
        # Highlight best route source/dest nodes
        if nodes:
            lines.append(f'  "{nodes[0]}" [fillcolor="#064e3b", color="#10b981", fontcolor="#34d399"];')
            lines.append(f'  "{nodes[-1]}" [fillcolor="#1e1b4b", color="#6366f1", fontcolor="#a5b4fc"];')

    added_edges = set()
    for route in routes:
        path = route.get("path", [])
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if (u, v) in added_edges:
                continue
            if (u, v) in best_path_edges:
                lines.append(f'  "{u}" -> "{v}" [color="#10b981", penwidth=3.0, '
                             f'arrowsize=1.2, label=" eco"];')
            else:
                lines.append(f'  "{u}" -> "{v}" [color="#475569", style=dashed, '
                             f'penwidth=1.0, arrowsize=0.8];')
            added_edges.add((u, v))

    lines.append("}")
    dot_source = "\n".join(lines)

    st.markdown('<div class="section-header">🗺️ Route Visualization</div>', unsafe_allow_html=True)
    st.graphviz_chart(dot_source, use_container_width=True)
=======
from __future__ import annotations

import streamlit as st


def render_map_view(path: list[str]) -> None:
    st.subheader("🗺️ Route Timeline")

    cols = st.columns(len(path)) if path else []
    for index, node in enumerate(path):
        cols[index].markdown(f"**{index + 1}. {node}**")
        if index < len(path) - 1:
            cols[index].caption("⬇")

    st.markdown("### Step-by-step")
    for index, node in enumerate(path, start=1):
        st.write(f"{index}. Arrive at node `{node}`")
>>>>>>> 8c3d578ab632eedee7d285f7a1cce0c2f1edc61d
