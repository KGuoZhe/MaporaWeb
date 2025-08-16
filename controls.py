# controls.py
# Display UI controls and return user selections as a dictionary

import streamlit as st

def show_controls(df):
    # Top control panel
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    view_mode = col1.radio("View mode", ["List", "Map"])
    sort_option = col2.selectbox("Sort by", ["Distance", "Rating"])

    # Region & city selection
    regions = {
        "North": ["Taipei City","New Taipei City","Taoyuan City","Keelung City","Hsinchu City","Hsinchu County","Yilan County","Miaoli County"],
        "Central": ["Taichung City","Changhua County","Nantou County","Yunlin County"],
        "South": ["Tainan City","Kaohsiung City","Chiayi City","Chiayi County","Pingtung County"],
        "East": ["Hualien County","Taitung County"],
        "Islands": ["Penghu County","Kinmen County","Lienchiang County"]
    }
    col_region, col_city = st.columns([1,1])
    selected_region = col_region.selectbox("Select region", list(regions.keys()))
    selected_city = col_city.selectbox("Select city", regions[selected_region])

    # Manual & auto location buttons
    col_manual, col_auto = st.columns([1,1])
    manual_loc_btn = col_manual.button("🗺️ Manual Location")
    auto_loc_btn = col_auto.button("📌 Auto Location")

    # Radius slider
    radius = col4.slider("Radius (m)", min_value=100, max_value=10000, value=500, step=100)

    # Search bar & category selection
    col_search, col_category = st.columns([3,1])
    search_query = col_search.text_input("Search", placeholder="Type a keyword...")
    category = col_category.selectbox("Category", ["All", "Food", "Sight"])

    # Feature filter selection
    feature_options = ["💲 Cheap","🏛 Traditional","🤫 Quiet","☕ Cozy","⚡ Fast service","🔥 Popular","🌳 Outdoor seating","🌊 Scenic"]
    selected_features = st.multiselect("Filter by feature", feature_options)

    return {
        "view_mode": view_mode,
        "sort_option": sort_option,
        "selected_region": selected_region,
        "selected_city": selected_city,
        "manual_loc_btn": manual_loc_btn,
        "auto_loc_btn": auto_loc_btn,
        "radius": radius,
        "search_query": search_query,
        "category": category,
        "selected_features": selected_features,
        "feature_options": feature_options
    }
