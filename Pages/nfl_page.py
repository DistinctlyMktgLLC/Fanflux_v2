# Pages/nfl_page.py
import streamlit as st
import pandas as pd
from utils import display_fan_demographics, apply_common_styles, load_data
from streamlit_folium import folium_static
import folium

def app():
    st.title("NFL Fans Analysis")
    
    # Apply common styles
    apply_common_styles()
    
    # Load the cleaned data
    df = load_data()
    
    # Sidebar filters
    selected_teams = st.sidebar.multiselect("Select Teams", df['Team'].unique())
    selected_leagues = st.sidebar.multiselect("Select Leagues", df['League'].unique())
    selected_fandom_level = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique())
    selected_race = st.sidebar.multiselect("Select Race", df['Race'].unique())
    selected_income_level = st.sidebar.multiselect("Select Income Level", df.columns[3:])

    # Apply filters to the dataframe
    if selected_teams:
        df = df[df['Team'].isin(selected_teams)]
    if selected_leagues:
        df = df[df['League'].isin(selected_leagues)]
    if selected_fandom_level:
        df = df[df['Fandom Level'].isin(selected_fandom_level)]
    if selected_race:
        df = df[df['Race'].isin(selected_race)]
    if selected_income_level:
        df = df[['Fandom Level', 'Race', 'League', 'Team'] + selected_income_level]

    # Display fan demographics
    display_fan_demographics(df)

    # Add map visualization
    if not df.empty:
        m = folium.Map(location=[37.7749, -122.4194], zoom_start=5)
        for idx, row in df.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=5,
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m)
        folium_static(m)
    else:
        st.write("No data available for the selected filters.")
