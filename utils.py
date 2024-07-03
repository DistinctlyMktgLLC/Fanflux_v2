import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from st_aggrid import AgGrid, GridOptionsBuilder

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
                popup=folium.Popup(
                    f"<b>Team:</b> {row['Team']}<br>"
                    f"<b>League:</b> {row['League']}<br>"
                    f"<b>Neighborhood:</b> {row['Neighborhood']}<br>"
                    f"<b>Fandom Level:</b> {row['Fandom Level']}<br>"
                    f"<b>Race:</b> {row['Race']}<br>"
                    f"<b>Total Fans:</b> {row['Total Fans']}",
                    max_width=300
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
        .scorecard {
            background-color: black;
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            color: white;
        }
        .scorecard .label {
            padding: 5px;
            margin: 5px;
            border-radius: 3px;
        }
        .scorecard .avid {
            background-color: #FFD700; /* Yellow */
        }
        .scorecard .casual {
            background-color: #00FF00; /* Green */
        }
        .scorecard .convertible {
            background-color: #FF4500; /* Red */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
