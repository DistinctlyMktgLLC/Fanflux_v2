import streamlit as st
import pandas as pd
from utils import display_fan_demographics, apply_common_styles

def app():
    apply_common_styles()
    
    # Load your parquet file
    df = pd.read_parquet("data/Fanflux_Intensity_All_Leagues_Cleaned.parquet")

    st.title("Fanflux League Analysis")
    
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

    filtered_df = df.copy()
    if leagues:
        filtered_df = filtered_df[filtered_df['League'].isin(leagues)]
    if teams:
        filtered_df = filtered_df[filtered_df['Team'].isin(teams)]
    if fandom_levels:
        filtered_df = filtered_df[filtered_df['Fandom Level'].isin(fandom_levels)]
    if races:
        filtered_df = filtered_df[filtered_df['Race'].isin(races)]
    if income_levels:
        filtered_df = filtered_df[filtered_df['Income Level'].isin(income_levels)]

    display_fan_demographics(filtered_df)
