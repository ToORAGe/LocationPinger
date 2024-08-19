import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
from sqlalchemy import create_engine, text
import os
import sqlite3

# Use the same absolute path as in the Flask app
db_path = os.path.join(os.path.dirname(__file__), 'locations.db')
db_uri = f'sqlite:///{db_path}'
print(f"Database path: {db_path}")
# Create an SQLAlchemy engine
engine = create_engine(db_uri)

# # Fetch all location data from the database
# def fetch_all_locations():
#     with engine.connect() as connection, connection.begin():
#         query = text("SELECT latitude, longitude FROM 'locations'")
#         locations_df = pd.read_sql(query, connection)
#     return locations_df

def fetch_all_locations(db_path: str) -> pd.DataFrame:
    # Establish a connection to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Define the query to fetch location data
    query = "SELECT latitude, longitude FROM location"
    
    # Fetch all location data from the database
    try:
        # Use Pandas to read the SQL query into a DataFrame
        locations_df = pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        locations_df = pd.DataFrame()  # Return an empty DataFrame in case of error
    finally:
        # Close the connection
        conn.close()
    
    return locations_df

# Fetch the latest location data from the server
def fetch_latest_location():
    response = requests.get("https://warm-memes-obey.loca.lt/location")  # Replace with your server URL
    if response.status_code == 200:
        location_data = response.json()
        return location_data['latitude'], location_data['longitude']
    return None, None

# Streamlit UI setup
st.title("Live Location Map with Spline Path")

# Fetch location data
locations_df = fetch_all_locations(db_path)

if not locations_df.empty:
    # Define the path layer
    path_layer = pdk.Layer(
        "PathLayer",
        data=[{
            "path": locations_df[['longitude', 'latitude']].values.tolist(),
            "color": [255, 0, 0],
            "width": 5,
        }],
        get_path="path",
        get_color="color",
        width_scale=20,
        width_min_pixels=2,
        width_max_pixels=10,
        rounded=True,
    )

    # Define the map view
    view_state = pdk.ViewState(
        latitude=locations_df['latitude'].mean(),
        longitude=locations_df['longitude'].mean(),
        zoom=14,
        pitch=50,
    )

    # Create the deck.gl map
    deck = pdk.Deck(
        layers=[path_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9",
    )

    # Render the map in Streamlit
    st.pydeck_chart(deck)
else:
    st.write("No location data available.")
