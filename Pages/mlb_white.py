import streamlit as st
import utils

def app():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.title("White Baseball Fans Analysis")

    df = utils.load_data("path_to_data/white_baseball_fans.parquet")
    
    st.sidebar.header("Filters")
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    income_level = st.sidebar.selectbox('Select Income Levels', ['Choose an option'] + sorted(df.columns[df.columns.str.contains('[$]')]))

    if team != 'Choose an option':
        df = df[df['Team'] == team]

    if income_level != 'Choose an option':
        df = df[df[income_level] > 0]

    st.header("Fan Opportunity Map")
    m = utils.create_map()
    color_key = {'Avid': 'red', 'Casual': 'orange', 'Convertible': 'green'}
    utils.add_map_markers(m, df, 'Fandom Level', color_key)
    st_folium(m, width=700, height=500)

    st.header("Fan Data Table")
    columns_to_display = ['Team', 'League', 'Neighborhood', 'Fandom Level', 'Race', 'Total Fans']
    df_display = df[columns_to_display]
    st.dataframe(df_display)
