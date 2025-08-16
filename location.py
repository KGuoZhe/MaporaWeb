# location.py
# Handle manual and automatic location selection

import streamlit as st
from streamlit_folium import st_folium
import folium
import streamlit.components.v1 as components

def manual_location_map():
    # Show Folium map for user to click location
    st.write("Click on the map to select a location.")
    m = folium.Map(location=[23.6978, 120.9605], zoom_start=7)  # Taiwan center
    m.add_child(folium.LatLngPopup())
    map_data = st_folium(m, width=700, height=500)

    if map_data and map_data["last_clicked"]:
        lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        st.success(f"Selected location: {lat}, {lon}")
        # TODO: Return coordinates to filter results / integrate with Google Maps API

def auto_location_script():
    # Use JavaScript Geolocation API to get user's current location
    components.html("""
        <script>
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                window.parent.postMessage({lat: lat, lon: lon}, "*");
            },
            function(error) {
                alert("Unable to retrieve your location: " + error.message);
            }
        );
        </script>
    """, height=0)
    # TODO: Capture returned coordinates and pass to result filtering / Google Maps API
