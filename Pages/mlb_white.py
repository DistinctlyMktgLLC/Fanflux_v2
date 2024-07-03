import streamlit as st
import utils
import pandas as pd
import numpy as np

def app():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")

    # Load data
    file_path = "data/Fanflux_Intensity_MLB_White.parquet"
    df = utils.load_data(file_path)

    # Sidebar filters
    st.sidebar.title("Filters")
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    league = st.sidebar.selectbox('Select a League', ['Choose an option'] + sorted(df['League'].unique()))
    income_level = st.sidebar.selectbox('Select Income Levels', ['Choose an option'] + sorted(df['Income Levels'].unique()))
    fandom_level = st.sidebar.selectbox('Select Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))

    if team != 'Choose an option':
        df = df[df['Team'] == team]
    if league != 'Choose an option':
        df = df[df['League'] == league]
    if income_level != 'Choose an option':
        df = df[df['Income Levels'] == income_level]
    if fandom_level != 'Choose an option':
        df = df[df['Fandom Level'] == fandom_level]

    # Create map
    m = utils.create_map()
    color_key = {'Avid': 'red', 'Casual': 'green', 'Convertible': 'blue'}
    utils.add_map_markers(m, df, 'Fandom Level', color_key)
    st.components.v1.html(m._repr_html_(), width=800, height=500)

    # Display data in AgGrid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    gb.configure_grid_options(domLayout='normal')
    gb.configure_columns(
        [
            "Team", "League", "City", "Neighborhood", "zipcode", 
            "US lat", "US lon", "Intensity", "Fandom Level", "Race"
        ],
        visible=False
    )
    gridOptions = gb.build()
    AgGrid(df, gridOptions=gridOptions, theme='streamlit')

if __name__ == "__main__":
    app()
