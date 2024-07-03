import streamlit as st
import utils

def app():
    utils.apply_common_styles()

    st.sidebar.title("Fanflux Navigation")
    page = st.sidebar.selectbox("Select a page", ["White Baseball Fans"])
    st.title("White Baseball Fans")

    df = utils.load_data("data/Fanflux_Intensity_MLB_White.parquet")

    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    income_level = st.sidebar.selectbox('Select Income Levels', ['Choose an option'] + sorted(df['Income Levels'].unique()))

    filtered_df = df[(df['Team'] == team) & (df['Income Levels'] == income_level)] if team != 'Choose an option' and income_level != 'Choose an option' else df

    gb = utils.create_grid_options(filtered_df)
    grid_response = st.datatable(filtered_df, gridOptions=gb, height=500, width='100%', reload_data=True)

    m = utils.create_map()
    utils.add_map_markers(m, filtered_df, 'Fandom Level', {
        'Avid': 'red',
        'Casual': 'blue',
        'Convertible': 'green'
    })
    st_folium(m, width=700, height=500)
