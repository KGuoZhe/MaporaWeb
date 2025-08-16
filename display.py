# display.py
# Filter data and show results in List or Map view

import streamlit as st
from utils import feature_badge

def display_results(df, user_inputs):
    filtered_df = df.copy()

    # Filter by city
    filtered_df = filtered_df[filtered_df['address'].str.contains(user_inputs["selected_city"], case=False, na=False)]

    # Filter by search query
    if user_inputs["search_query"].strip():
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(user_inputs["search_query"], case=False, na=False) |
            filtered_df["features"].apply(lambda x: any(user_inputs["search_query"].lower() in f.lower() for f in x))
        ]

    # Filter by features
    if user_inputs["selected_features"]:
        feature_mapping = {opt.split(" ",1)[1]: opt for opt in user_inputs["feature_options"]}
        filter_feature_names = [k for k,v in feature_mapping.items() if v in user_inputs["selected_features"]]
        filtered_df = filtered_df[filtered_df["features"].apply(lambda x: any(f in x for f in filter_feature_names))]

    # Filter by radius
    filtered_df = filtered_df[filtered_df["distance"] <= user_inputs["radius"]]

    # Sort results
    if user_inputs["sort_option"]=="Distance":
        filtered_df = filtered_df.sort_values(by="distance", ascending=True)
    elif user_inputs["sort_option"]=="Rating":
        filtered_df = filtered_df.sort_values(by="rating", ascending=False)

    # Filter by category
    if user_inputs["category"]!="All" and "type" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["type"].str.strip().str.lower()==user_inputs["category"].lower()]

    # Display results
    if user_inputs["view_mode"]=="List":
        for i, (_, row) in enumerate(filtered_df.iterrows()):
            bg_color = "#F9F9F9" if i%2==0 else "#FFFFFF"
            with st.container():
                st.markdown(f"<div style='background-color:{bg_color}; padding:10px; border-radius:10px;'>", unsafe_allow_html=True)
                col1, col2 = st.columns([1,3])
                with col1:
                    st.image(row["image"], use_column_width=True)
                with col2:
                    st.markdown(f"### {row['name']}")
                    badges = " ".join([feature_badge(f) for f in row["features"]])
                    st.markdown(badges, unsafe_allow_html=True)
                    st.write(f"📍 {row['address']}")
                    st.write(f"⭐ {row['rating']}  |  📏 {row['distance']} m")
                    st.write(f"📝 Review: {row['review']}")
                    st.write(f"💡 Summary: {row['summary']}")
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.write("🗺️ Map view will be replaced with Google Maps API integration")  # TODO: Insert Google Maps API here
    # TODO: Replace df iteration with Google API results