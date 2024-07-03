import streamlit as st
import pandas as pd
import folium
from st_aggrid import AgGrid, GridOptionsBuilder

def load_data(race):
    file_path = f'data/Fanflux_Intensity_MLB_{race}.parquet'
    try:
        return pd.read_parquet(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

def create_map():
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    return m

def add_map_markers(m, df, color_column, color_key):
    for _, row in df.iterrows():
        try:
            folium.CircleMarker(
                location=[row['US lat'], row['US lon']],
                radius=5,
                color=color_key.get(row[color_column], 'blue'),
                fill=True,
                fill_color=color_key.get(row[color_column], 'blue'),
                tooltip=folium.Tooltip(
                    f"Team: {row['Team']}<br>"
                    f"League: {row['League']}<br>"
                    f"Neighborhood: {row['Neighborhood']}<br>"
                    f"Fan Type: {row['Fandom Level']}<br>"
                    f"Race: {row['Race']}"
                )
            ).add_to(m)
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

def render_aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    gb.configure_default_column(hide=True)  # Hide all columns by default
    gb.configure_column("Team", hide=False)
    gb.configure_column("League", hide=False)
    gb.configure_column("Neighborhood", hide=False)
    gb.configure_column("zipcode", hide=False)
    gb.configure_column("Intensity", hide=False)
    gb.configure_column("Fandom Level", hide=False)
    gb.configure_column("Race", hide=False)
    return AgGrid(df, gridOptions=gb.build(), height=500)
