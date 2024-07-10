import streamlit as st
import pandas as pd
from utils import display_fan_demographics, apply_common_styles
import leafmap.foliumap as leafmap

def app():
    st.title("Fanflux League Analysis")

    # Read the combined Parquet file
    df = pd.read_parquet('data/combined_leagues.parquet')

    leagues = st.multiselect("Select Leagues", options=df['League'].unique())
    teams = st.multiselect("Select Teams", options=df['Team'].unique())
    fandom_levels = st.multiselect("Select Fandom Levels", options=['Avid', 'Casual', 'Convertible'])
    races = st.multiselect("Select Races", options=df['Race'].unique())
    income_levels = st.multiselect("Select Income Levels", options=[
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
        'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
        'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
        'Affluent ($200,000 or more)'
    ])

    # Apply filters
    if leagues:
        df = df[df['League'].isin(leagues)]
    if teams:
        df = df[df['Team'].isin(teams)]
    if fandom_levels:
        df = df[df['Fandom Level'].isin(fandom_levels)]
    if races:
        df = df[df['Race'].isin(races)]
    if income_levels:
        df = df[df[income_levels].any(axis=1)]

    display_fan_demographics(df)

    st.subheader("Fan Opportunity Map")
    
    # Filter out rows with NaN values in 'US lat' or 'US lon'
    df = df.dropna(subset=['US lat', 'US lon'])

    m = leafmap.Map(center=[37.7749, -122.4194], zoom=4)
    for i, row in df.iterrows():
        m.add_marker(location=[row['US lat'], row['US lon']], tooltip=f"Team: {row['Team']}<br>League: {row['League']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}<br>Income Level: {row['Income Level']}")
    m.to_streamlit(height=600)
