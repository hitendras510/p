import streamlit as st
from components.route_card import CITY_NODES, NODE_COORDS


def render_map_view(result: dict) -> None:
    """
    Renders a Graphviz route visualization showing both the eco route
    and shortest route on the same graph. Additionally renders a Leaflet
    map embed for real-world visualization.
    """
    eco_path = result.get("route", [])
    shortest_path = result.get("shortest_route", [])

    if not eco_path:
        st.info("No route to display.")
        return

    # ---- Graphviz Network Graph ----
    st.markdown('<div class="section-header">🗺️ Route Network</div>', unsafe_allow_html=True)

    eco_edges = set()
    for i in range(len(eco_path) - 1):
        eco_edges.add((eco_path[i], eco_path[i + 1]))

    short_edges = set()
    for i in range(len(shortest_path) - 1):
        short_edges.add((shortest_path[i], shortest_path[i + 1]))

    # All graph edges (from route_service.py)
    all_graph_edges = [
        ("A", "B", 5, 10), ("A", "C", 8, 3),
        ("B", "D", 2, 2), ("C", "D", 4, 6),
        ("C", "E", 7, 1), ("D", "E", 1, 2),
        ("D", "F", 6, 8), ("E", "F", 3, 1),
    ]

    lines = []
    lines.append("digraph EcoNav {")
    lines.append("  rankdir=LR;")
    lines.append('  bgcolor="transparent";')
    lines.append("  pad=0.5; nodesep=0.8; ranksep=1.2;")
    lines.append('  node [shape=box, style="rounded,filled", fontname="Inter", fontsize=11, '
                 'fillcolor="#1e293b", fontcolor="#e2e8f0", color="#334155", penwidth=1.5];')
    lines.append('  edge [fontname="Inter", fontsize=9];')

    # Node labels with city names
    for node, city in CITY_NODES.items():
        if node == eco_path[0]:
            lines.append(f'  "{node}" [label="{city}", fillcolor="#064e3b", color="#10b981", fontcolor="#34d399"];')
        elif node == eco_path[-1]:
            lines.append(f'  "{node}" [label="{city}", fillcolor="#1e1b4b", color="#6366f1", fontcolor="#a5b4fc"];')
        else:
            lines.append(f'  "{node}" [label="{city}"];')

    # Draw edges
    for u, v, dist, pol in all_graph_edges:
        edge_label = f"{dist}km, AQI:{pol}"
        if (u, v) in eco_edges:
            lines.append(f'  "{u}" -> "{v}" [color="#10b981", penwidth=3.0, '
                         f'arrowsize=1.2, label=" {edge_label}", fontcolor="#34d399"];')
        elif (u, v) in short_edges:
            lines.append(f'  "{u}" -> "{v}" [color="#ef4444", penwidth=2.0, '
                         f'style=dashed, label=" {edge_label}", fontcolor="#f87171"];')
        else:
            lines.append(f'  "{u}" -> "{v}" [color="#334155", penwidth=1.0, '
                         f'arrowsize=0.7, label=" {edge_label}", fontcolor="#475569"];')

    # Legend
    lines.append('  subgraph cluster_legend {')
    lines.append('    label="Legend"; fontname="Inter"; fontsize=10; fontcolor="#94a3b8";')
    lines.append('    style="rounded"; color="#1e293b";')
    lines.append('    L1 [label="🟢 Eco Route", shape=plaintext, fontcolor="#34d399"];')
    lines.append('    L2 [label="🔴 Shortest Route", shape=plaintext, fontcolor="#f87171"];')
    lines.append('  }')

    lines.append("}")
    dot_source = "\n".join(lines)

    st.graphviz_chart(dot_source, use_container_width=True)

    # ---- Leaflet Map Embed ----
    st.markdown('<div class="section-header">🌍 Real-World Map</div>', unsafe_allow_html=True)

    # Build Leaflet HTML for the eco route
    eco_coords_js = ", ".join(
        f"[{NODE_COORDS[n][0]}, {NODE_COORDS[n][1]}]" for n in eco_path if n in NODE_COORDS
    )
    short_coords_js = ", ".join(
        f"[{NODE_COORDS[n][0]}, {NODE_COORDS[n][1]}]" for n in shortest_path if n in NODE_COORDS
    )
    markers_js = ""
    for n in set(eco_path + shortest_path):
        if n in NODE_COORDS:
            city = CITY_NODES.get(n, n)
            markers_js += f'L.marker([{NODE_COORDS[n][0]}, {NODE_COORDS[n][1]}]).addTo(map).bindPopup("{city} ({n})");\n'

    map_html = f"""
    <div style="border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.08);">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <div id="map" style="height: 400px; width: 100%;"></div>
    <script>
        var map = L.map('map').setView([26, 80], 6);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap'
        }}).addTo(map);

        // Shortest route (red dashed)
        var shortCoords = [{short_coords_js}];
        L.polyline(shortCoords, {{color: '#ef4444', weight: 4, opacity: 0.6, dashArray: '10,6'}}).addTo(map);

        // Eco route (green solid)
        var ecoCoords = [{eco_coords_js}];
        L.polyline(ecoCoords, {{color: '#10b981', weight: 6, opacity: 0.9}}).addTo(map);

        // Markers
        {markers_js}

        map.fitBounds(L.polyline(ecoCoords).getBounds(), {{padding: [30, 30]}});
    </script>
    </div>
    """
    st.components.v1.html(map_html, height=430)
