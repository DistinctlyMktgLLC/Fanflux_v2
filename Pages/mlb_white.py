import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import leafmap.foliumap as leafmap

def display_scorecards(df):
    avid_count = df[df['Fandom Level'] == 'Avid'].shape[0]
    casual_count = df[df['Fandom Level'] == 'Casual'].shape[0]
    convertible_count = df[df['Fandom Level'] == 'Convertible'].shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avid Fans", avid_count)
    with col2:
        st.metric("Casual Fans", casual_count)
    with col3:
        st.metric("Convertible Fans", convertible_count)

def display_table(df):
    AgGrid(df, height=400, width='100%', theme='streamlit', fit_columns_on_grid_load=True)

def interactive_map():
    col1, col2 = st.columns([4, 1])
    options = list(leafmap.basemaps.keys())
    index = options.index("OpenTopoMap")

    with col2:
        basemap = st.selectbox("Select a basemap:", options, index)
    with col1:
        m = leafmap.Map(
            locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
        )
        m.add_basemap(basemap)
        m.to_streamlit(height=700)

def app():
    st.title("White Baseball Fans")

    # Load data
    df = pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")

    if df.empty:
        st.error("No data available.")
        return

    # Display scorecards
    display_scorecards(df)

    # Display table
    display_table(df)

    # Display interactive map
    interactive_map()

if __name__ == "__main__":
    app()
