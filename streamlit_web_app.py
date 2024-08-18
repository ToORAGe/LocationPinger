import streamlit as st
from streamlit_autorefresh import st_autorefresh
import time
import pandas as pd
import requests

# Function to get the current location from your server
def get_location():
    try:
        response = requests.get("http://127.0.0.1:5000/latest-location")  # Replace with your actual server URL
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch location data from server.")
            return None
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

# Streamlit app layout
st.title("Live Location Tracker")

# Auto-refresh every 2 seconds
st_autorefresh(interval=10000, limit=100, key="location_autorefresh")

# Create a placeholder for the map
map_placeholder = st.empty()

# Fetch and display location
location_data = get_location()
if location_data:
    lat = location_data.get("latitude")
    lon = location_data.get("longitude")
    
    # Example to display location on the map
    df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    map_placeholder.map(df)
