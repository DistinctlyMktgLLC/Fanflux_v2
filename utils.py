import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from st_aggrid import AgGrid, GridOptionsBuilder
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
                popup=f"""
                <b>Team:</b> {row['Team']}<br>
                <b>League:</b> {row['League']}<br>
                <b>Neighborhood:</b> {row['Neighborhood']}<br>
                <b>Fan Type:</b> {row['Fandom Level']}<br>
                <b>Race:</b> {row['Race']}<br>
                <b>Total Fans:</b> {sum(row[['Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)', 'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)', 'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)']])}
                """
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
        .ag-theme-streamlit {
            --ag-header-background-color: #f8f9fa;
            --ag-odd-row-background-color: #ffffff;
            --ag-row-hover-color: #e9ecef;
        }
        .stCard {
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 5px solid;
            padding: 15px;
            margin: 10px 0;
        }
        .avid {
            border-color: #FF0000;
        }
        .casual {
            border-color: #00FF00;
        }
        .convertible {
            border-color: #0000FF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
