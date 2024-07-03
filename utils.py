import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components

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
                    f"Total Fans: {sum([row[col] for col in df.columns if '$' in col])}"
                )
            ).add_to(marker_cluster)
        except KeyError as e:
            st.error(f"Column not found: {e}")

def create_table(df):
    html = df.to_html(classes='table table-striped')
    components.html(html, height=600, scrolling=True)

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
        .table {
            width: 100%;
            margin-bottom: 1rem;
            color: #212529;
        }
        .table th,
        .table td {
            padding: 0.75rem;
            vertical-align: top;
            border-top: 1px solid #dee2e6;
        }
        .table thead th {
            vertical-align: bottom;
            border-bottom: 2px solid #dee2e6;
        }
        .table tbody + tbody {
            border-top: 2px solid #dee2e6;
        }
        .table .table {
            background-color: #fff;
        }
        .table-striped tbody tr:nth-of-type(odd) {
            background-color: rgba(0, 0, 0, 0.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
