# services/google_maps.py
# ======================
# Google Maps / Places API helper functions
# This module handles requests to Google Places API using the API Key from config.py
# ======================

import requests
from config import GOOGLE_API_KEY

# ----------------------
# Search places by keyword and location
# ----------------------
def search_places(query: str, location: str, radius: int = 5000, place_type: str = "restaurant"):
    """
    Search places using Google Places Text Search API.
    query: search keyword, e.g., "Taipei night market"
    location: "lat,lng" string, e.g., "25.0330,121.5654"
    radius: search radius in meters
    place_type: type of place, e.g., restaurant, tourist_attraction
    Returns: JSON response from Google Places API
    """
    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={query}"
        f"&location={location}"
        f"&radius={radius}"
        f"&type={place_type}"
        f"&key={GOOGLE_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        return {"error": f"API request failed with status {response.status_code}"}

# ----------------------
# Search top places by city and category
# ----------------------
def search_top_places(city: str, category: str, max_results: int = 15):
    """
    Get top places for a city and category using Google Places API.
    city: e.g., "Taipei City"
    category: "Food" -> "restaurant", "Sight" -> "tourist_attraction"
    max_results: number of results to return
    """
    place_type = "restaurant" if category.lower() == "food" else "tourist_attraction"
    
    # Use Text Search API with "popular" keyword
    query = f"popular {category.lower()} in {city}"
    
    # Use approximate city center coordinates (can later refine with Google Geocoding API)
    city_coords = {
        "Taipei City": "25.0330,121.5654",
        "New Taipei City": "25.0169,121.4628",
        "Taichung City": "24.1477,120.6736",
        "Tainan City": "22.9999,120.2270",
        "Kaohsiung City": "22.6273,120.3014"
        # can add other cities
    }
    location = city_coords.get(city, "23.6978,120.9605")  # default to Taiwan center

    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={query}"
        f"&location={location}"
        f"&radius=5000"
        f"&type={place_type}"
        f"&key={GOOGLE_API_KEY}"
    )
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Get top max_results
        return data.get("results", [])[:max_results]
    else:
        return {"error": f"API request failed with status {response.status_code}"}
