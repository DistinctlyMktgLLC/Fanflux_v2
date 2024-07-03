import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

def load_data(file_path):
    try:
        return pd.read_parquet(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

def create_map():
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    return m

def add_map_markers(m, df, color_column, color_key):
    for _, row in df.iterrows():
        try:
            tooltip_content = f"""
            <b>Team:</b> {row['Team']}<br>
            <b>League:</b> {row['League']}<br>
            <b>Neighborhood:</b> {row['Neighborhood']}<br>
            <b>Fan Type:</b> {row['Fandom Level']}<br>
            <b>Race:</b> {row['Race']}
            """
            m.add_point(
                lat=row['US lat'],
                lon=row['US lon'],
                popup=tooltip_content,
                color=color_key.get(row[color_column], 'blue')
            )
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
        </style>
        """,
        unsafe_allow_html=True
    )
