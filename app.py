# app.py
# Main application: orchestrates data loading, UI controls, location selection, and result display

import streamlit as st
from utils import load_data
from controls import show_controls
from location import manual_location_map, auto_location_script
from display import display_results
from config import USE_GOOGLE_API
from services.google_maps import search_places, search_top_places
import pandas as pd

# Load CSV data
df = load_data("fake_data.csv")  # TODO: Replace with Google Places API data in future

# Page setup
st.set_page_config(page_title="Mapora Web", layout="wide")
st.title("Mapora Web 🍽️")
st.subheader("Find places to eat or visit in Taiwan")

# Show control panel and get user inputs
user_inputs = show_controls(df)

# Handle location selection
if user_inputs["manual_loc_btn"]:
    manual_location_map()  # Returns coordinates via folium map
if user_inputs["auto_loc_btn"]:
    auto_location_script()  # Returns coordinates via browser geolocation

# ---------- Google API integration ----------
city = user_inputs["selected_city"]
category = user_inputs["category"]

if USE_GOOGLE_API:
    # If user typed something in search bar, use search_places
    if user_inputs["search_query"].strip():
        results = search_places(
            query=user_inputs["search_query"],
            location="25.0330,121.5654",  # default location, can improve later
            radius=user_inputs["radius"]
        )
    else:
        # No search input: grab top/popular places for city & category
        results = search_top_places(city, category, max_results=15)

    # Normalize Google API results to DataFrame
    rows = []
    for place in results:
        if "error" in place:
            continue
        # Get image URL if photos exist
        if place.get("photos"):
            photo_ref = place["photos"][0]["photo_reference"]
            image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={place.get('GOOGLE_API_KEY', '')}"
        else:
            image_url = ""
        rows.append({
            "name": place.get("name", ""),
            "address": place.get("formatted_address", ""),
            "type": category,
            "rating": place.get("rating", 0),
            "features": [],
            "image": image_url,
            "distance": 0,  # TODO: calculate actual distance later
            "review": "No review yet",
            "summary": "No summary yet"
        })

    df = pd.DataFrame(rows)
    display_results(df, user_inputs)
else:
    # CSV fallback
    display_results(df, user_inputs)
