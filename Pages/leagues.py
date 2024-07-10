import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from utils import display_fan_demographics

# Load data
df = pd.read_parquet('data/combined_leagues.parquet')

def app():
    leagues = st.multiselect("Select Leagues", options=df['League'].unique())
    teams = st.multiselect("Select Teams", options=df['Team'].unique())
    fandom_levels = st.multiselect("Select Fandom Levels", options=df['Fandom Level'].unique())
    races = st.multiselect("Select Races", options=df['Race'].unique())
    income_levels = st.multiselect("Select Income Levels", options=df.columns[12:])

    filtered_df = df[
        (df['League'].isin(leagues)) &
        (df['Team'].isin(teams)) &
        (df['Fandom Level'].isin(fandom_levels)) &
        (df['Race'].isin(races))
    ]

    if income_levels:
        income_mask = filtered_df[income_levels].apply(lambda row: row.sum(), axis=1) > 0
        filtered_df = filtered_df[income_mask]

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
