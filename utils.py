# utils.py
# Utility functions: load data, generate feature badges

import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['features'] = df['features'].apply(lambda x: x.split(";"))
    df['review'] = ["No review yet"] * len(df)
    df['summary'] = ["No summary yet"] * len(df)
    return df

def feature_badge(feature):
    # Return HTML span with color for each feature
    colors = {
        "Cheap": "#FFB6C1",
        "Traditional": "#ADD8E6",
        "Quiet": "#90EE90",
        "Cozy": "#FFD700",
        "Fast service": "#FFA07A",
        "Popular": "#FF69B4",
        "Outdoor seating": "#87CEFA",
        "Scenic": "#20B2AA",
        "Good coffee": "#D8BFD8"
    }
    color = colors.get(feature, "#D3D3D3")
    return f'<span style="background-color:{color}; padding:3px 6px; border-radius:5px; margin-right:3px;">{feature}</span>'
