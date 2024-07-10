import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from utils import display_fan_demographics

# Load the combined dataset
df = pd.read_parquet('data/combined_leagues.parquet')

# Define the app function
def app():
    st.title("Fanflux League Analysis")
    
    # Sidebar filters
    leagues = st.multiselect("Select Leagues", options=df['League'].unique())
    teams = st.multiselect("Select Teams", options=df['Team'].unique())
    fandom_levels = st.multiselect("Select Fandom Levels", options=df['Fandom Level'].unique())
    races = st.multiselect("Select Races", options=df['Race'].unique())
    income_levels = st.multiselect("Select Income Levels", options=df.columns[12:28].tolist())

    # Apply filters to the dataframe
    filtered_df = df.copy()
    
    if leagues:
        filtered_df = filtered_df[filtered_df['League'].isin(leagues)]
    if teams:
        filtered_df = filtered_df[filtered_df['Team'].isin(teams)]
    if fandom_levels:
        filtered_df = filtered_df[filtered_df['Fandom Level'].isin(fandom_levels)]
    if races:
        filtered_df = filtered_df[filtered_df['Race'].isin(races)]
    
    # Display fan demographics
    display_fan_demographics(filtered_df)
    
    # Create a map
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=5)
    
    # Add markers
    for _, row in filtered_df.iterrows():
        if pd.notna(row['US lat']) and pd.notna(row['US lon']):
            folium.Marker(
                location=[row['US lat'], row['US lon']],
                tooltip=f"Team: {row['Team']}<br>League: {row['League']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}"
            ).add_to(m)
    
    # Display the map
    folium_static(m)
