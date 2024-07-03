import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_aggrid import AgGrid, GridOptionsBuilder
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
            folium.CircleMarker(
                location=[row['US lat'], row['US lon']],
                radius=5,
                color=color_key.get(row[color_column], 'blue'),
                fill=True,
                fill_color=color_key.get(row[color_column], 'blue'),
                tooltip=(
                    f"Team: {row['Team']}<br>"
                    f"League: {row['League']}<br>"
                    f"Neighborhood: {row['Neighborhood']}<br>"
                    f"Fan Type: {row['Fandom Level']}<br>"
                    f"Race: {row['Race']}<br>"
                    f"Total Fans: {row['total_fans']}"
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
        .stAgGrid-main {
            height: 500px;
        }
        .ag-theme-dark {
            --ag-background-color: #2E2E2E;
            --ag-border-color: #000;
            --ag-row-hover-color: #444;
            --ag-header-background-color: #555;
            --ag-font-color: #fff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
