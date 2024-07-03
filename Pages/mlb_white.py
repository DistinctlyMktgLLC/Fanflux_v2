import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_aggrid import AgGrid, GridOptionsBuilder
from folium.plugins import MarkerCluster
import utils

def app():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")

    df = utils.load_data('data/Fanflux_Intensity_MLB_White.parquet')
    
    st.sidebar.header("Filters")
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    league = st.sidebar.selectbox('Select a League', ['Choose an option'] + sorted(df['League'].unique()))
    fandom_level = st.sidebar.selectbox('Select Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))

    filtered_df = df
    if team != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Team'] == team]
    if league != 'Choose an option':
        filtered_df = filtered_df[filtered_df['League'] == league]
    if fandom_level != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Fandom Level'] == fandom_level]

    st.title("White Baseball Fans")
    avid_fans = filtered_df[filtered_df['Fandom Level'] == 'Avid'].shape[0]
    casual_fans = filtered_df[filtered_df['Fandom Level'] == 'Casual'].shape[0]
    convertible_fans = filtered_df[filtered_df['Fandom Level'] == 'Convertible'].shape[0]

    st.metric("Avid Fans", avid_fans)
    st.metric("Casual Fans", casual_fans)
    st.metric("Convertible Fans", convertible_fans)

    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    gb.configure_side_bar()
    gb.configure_default_column(editable=True, groupable=True)

    gridOptions = gb.build()

    st.header("Fan Opportunity Data")
    AgGrid(filtered_df, gridOptions=gridOptions, height=400, theme='dark')

    st.header("Fan Opportunity Map")
    m = utils.create_map()

    color_key = {
        'Avid': 'green',
        'Casual': 'yellow',
        'Convertible': 'red'
    }

    utils.add_map_markers(m, filtered_df, 'Fandom Level', color_key)

    st_folium(m, width=1200, height=600)

    utils.apply_common_styles()
