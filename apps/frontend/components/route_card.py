import streamlit as st

def render_route_card(route_data: dict, is_best_route: bool = False):
    """
    Renders a Streamlit component displaying details for a specific route.
    
    Args:
        route_data (dict): Dictionary containing 'path', 'distance', 'traffic', etc.
        is_best_route (bool): Whether this is the AI-recommended optimal route.
    """
    # Create a visual container for the card
    with st.container():
        # Add a border and some highlighting if it's the best route
        if is_best_route:
            st.success("🌿 EcoNav Recommended Route")
            
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Distance", value=f"{route_data.get('distance', 0)} km")
            
        with col2:
            st.metric(label="Traffic Level", value=route_data.get('traffic', 'Unknown'))
            
        with col3:
            # You can add exposure/AQI metrics here later
            st.metric(label="Exposure Score", value="Good") 
            
        # Display the path sequence
        path = route_data.get('path', [])
        st.markdown(f"**Path:** {' ➔ '.join(path)}")
        st.divider()
