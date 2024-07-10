import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from utils import display_fan_demographics, apply_common_styles

def app():
    apply_common_styles()

    # Load the combined dataset
    df = pd.read_parquet('data/combined_leagues.parquet')

    # Define income columns
    income_columns = [
        'struggling_(less_than_$10,000)', 'getting_by_($10,000_to_$14,999)', 'getting_by_($15,000_to_$19,999)',
        'starting_out_($20,000_to_$24,999)', 'starting_out_($25,000_to_$29,999)', 'starting_out_($30,000_to_$34,999)',
        'middle_class_($35,000_to_$39,999)', 'middle_class_($40,000_to_$44,999)', 'middle_class_($45,000_to_$49,999)',
        'comfortable_($50,000_to_$59,999)', 'comfortable_($60,000_to_$74,999)', 'doing_well_($75,000_to_$99,999)',
        'prosperous_($100,000_to_$124,999)', 'prosperous_($125,000_to_$149,999)', 'wealthy_($150,000_to_$199,999)',
        'affluent_($200,000_or_more)'
    ]

    # Filters
    leagues = st.multiselect("Select Leagues", options=df['league'].unique())
    teams = st.multiselect("Select Teams", options=df['team'].unique())
    fandom_levels = st.multiselect("Select Fandom Levels", options=['avid', 'casual', 'convertible'])
    races = st.multiselect("Select Races", options=df['race'].unique())
    income_levels = st.multiselect("Select Income Levels", options=income_columns)

    # Filter the dataset based on selections
    filtered_df = df[
        (df['league'].isin(leagues)) &
        (df['team'].isin(teams)) &
        (df['fandom_level'].isin(fandom_levels)) &
        (df['race'].isin(races))
    ]

    if income_levels:
        income_mask = filtered_df[income_columns].apply(lambda row: any(row[level] == 1.0 for level in income_levels), axis=1)
        filtered_df = filtered_df[income_mask]

    # Display fan demographics
    display_fan_demographics(filtered_df)

    # Create a map
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    # Add markers
    for _, row in filtered_df.iterrows():
        if pd.notna(row['us_lat']) and pd.notna(row['us_lon']):
            folium.Marker(
                location=[float(row['us_lat']), float(row['us_lon'])],
                tooltip=f"Team: {row['team']}<br>League: {row['league']}<br>Fandom Level: {row['fandom_level']}<br>Race: {row['race']}<br>Neighborhood: {row['neighborhood']}"
            ).add_to(m)

    # Display the map
    folium_static(m)
