import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

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
            folium.CircleMarker(
                location=[row['US lat'], row['US lon']],
                radius=5,
                color=color_key.get(row[color_column], 'blue'),
                fill=True,
                fill_color=color_key.get(row[color_column], 'blue'),
                fill_opacity=0.6,
                popup=(
                    f"Team: {row['Team']}<br>"
                    f"League: {row['League']}<br>"
                    f"Neighborhood: {row['Neighborhood']}<br>"
                    f"Fandom Level: {row['Fandom Level']}<br>"
                    f"Race: {row['Race']}<br>"
                    f"Total Fans: {row['Total Fans']}"
                )
            ).add_to(marker_cluster)
        except KeyError as e:
            st.error(f"Column not found: {e}")

def apply_common_styles():
    st.markdown(
        """
        <style>
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .stButton>button {
            color: #fff;
            background-color: #007bff;
            border-color: #007bff;
            border-radius: 4px;
        }
        .stButton>button:hover {
            color: #fff;
            background-color: #0056b3;
            border-color: #0056b3;
        }
        .dataframe {
            overflow-x: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
