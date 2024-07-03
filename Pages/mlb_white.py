import streamlit as st
import utils
import folium
from streamlit_folium import folium_static

def app():
    st.title('White Baseball Fans')

    # Filters
    team_options = st.selectbox('Select a Team', options=['Choose an option'])
    league_options = st.selectbox('Select a League', options=['Choose an option'])
    income_levels = st.multiselect('Select Income Levels', options=[
        'Getting By ($10,000 to $14,999)', 
        'Getting By ($15,000 to $19,999)', 
        'Starting Out ($20,000 to $24,999)',
        'Starting Out ($25,000 to $29,999)',
        'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)',
        'Middle Class ($40,000 to $49,999)',
        'Comfortable ($50,000 to $59,999)',
        'Comfortable ($60,000 to $74,999)',
        'Wealthy ($75,000 to $99,999)',
        'Wealthy ($100,000 to $124,999)',
        'Wealthy ($125,000 to $149,999)',
        'Wealthy ($150,000 and above)'
    ])
    fandom_levels = st.selectbox('Select a Fandom Level', options=['Choose an option'])

    # Load and filter data
    df = utils.load_and_filter_data('data/Fanflux_Intensity_MLB_White.parquet', selected_income_levels=income_levels)
    
    # Display the AgGrid table
    st.write("Fan Data Table")
    utils.display_aggrid_table(df)

    # Display the map
    st.write("Map Visualization")
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    color_key = {
        'Avid': 'green',
        'Casual': 'blue',
        'Convertible Fans': 'red'
    }
    utils.add_map_markers(m, df, 'Fandom Level', color_key)
    folium_static(m)
