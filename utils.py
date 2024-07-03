import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

def load_data(file_path):
    try:
        return pd.read_parquet(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

def create_map():
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    return m

def add_map_markers(m, df, color_column, color_key):
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        try:
            tooltip = f"""
                Team: {row['Team']}<br>
                League: {row['League']}<br>
                Neighborhood: {row['Neighborhood']}<br>
                Fan Type: {row['Fandom Level']}<br>
                Race: {row['Race']}<br>
                Total Fans: {row['Total Fans']}
            """
            folium.CircleMarker(
                location=[row['US lat'], row['US lon']],
                radius=5,
                color=color
