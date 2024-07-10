import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from utils import display_fan_demographics, apply_common_styles

def app():
    apply_common_styles()

    # Define income columns
    income_columns = [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
        'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
        'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
        'Affluent ($200,000 or more)'
    ]

    # Load the combined dataset
    df = pd.read_parquet('data/combined_leagues.parquet')

    # Filters
    leagues = st.multiselect("Select Leagues", options=df['League'].unique())
    teams = st.multiselect("Select Teams", options=df['Team'].unique())
    fandom_levels = st.multiselect("Select Fandom Levels", options=['Avid', 'Casual', 'Convertible'])
    races = st.multiselect("Select Races", options=df['Race'].unique())
    income_levels = st.multiselect("Select Income Levels", options=income_columns)

    # Filter the dataset based on selections
    filtered_df = df[
        (df['League'].isin(leagues)) &
        (df['Team'].isin(teams)) &
        (df['Fandom Level'].isin(fandom_levels)) &
        (df['Race'].isin(races))
    ]

    if income_levels:
        income_mask = filtered_df[income_columns].apply(lambda row: any(row[level] == '1.0' for level in income_levels), axis=1)
        filtered_df = filtered_df[income_mask]

    # Display fan demographics
    display_fan_demographics(filtered_df)

    # Create a map
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    # Add markers
    for _, row in filtered_df.iterrows():
        if pd.notna(row['US lat']) and pd.notna(row['US lon']):
            folium.Marker(
                location=[float(row['US lat']), float(row['US lon'])],
                tooltip=f"Team: {row['Team']}<br>League: {row['League']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}<br>Income Level: {row['Income Level']}"
            ).add_to(m)

    # Display the map
    folium_static(m)
