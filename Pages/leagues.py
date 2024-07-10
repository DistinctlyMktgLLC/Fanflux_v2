import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from utils import display_fan_demographics, apply_common_styles

def app():
    apply_common_styles()

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
