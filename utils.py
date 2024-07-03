import streamlit as st
import pandas as pd
import folium
from st_aggrid import AgGrid, GridOptionsBuilder
from folium.plugins import MarkerCluster

def load_data(race):
    file_path = f'data/Fanflux_Intensity_MLB_{race}.parquet'
    try:
        df = pd.read_parquet(file_path)
        df['zipcode'] = df['zipcode'].apply(lambda x: f"{int(x):05}")  # Ensure zip codes have leading zeros
        return df
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
                    f"Team: {row['Team']}<br>League: {row['League']}<br>Neighborhood: {row['Neighborhood']}<br>Fan Type: {row['Fandom Level']}<br>Race: {row['Race']}<br>Total Fans: {row['Total Fans']}",
                    sticky=False
                )
            ).add_to(m)
        except KeyError as e:
            st.error(f"Column not found: {e}")

def render_aggrid(df, enable_page=False):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=enable_page, paginationAutoPageSize=False, paginationPageSize=25)
    gb.configure_default_column(width=120)
    gridOptions = gb.build()
    AgGrid(df, gridOptions=gridOptions, height=500, width='100%', theme='streamlit', enable_enterprise_modules=True)

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
