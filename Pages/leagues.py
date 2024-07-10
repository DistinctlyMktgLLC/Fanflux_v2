import streamlit as st
import pandas as pd
from utils import display_fan_demographics, apply_common_styles

def app():
    # Load the cleaned parquet file
    df = pd.read_parquet("data/Fanflux_Intensity_All_Leagues_Cleaned_Final.parquet")

    st.title("Fanflux League Analysis")

    # Sidebar filters
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

    # Filter the dataframe based on selections
    filtered_df = df[
        (df['League'].isin(leagues)) &
        (df['Team'].isin(teams)) &
        (df['Fandom Level'].isin(fandom_levels)) &
        (df['Race'].isin(races))
    ]

    # Display the fan demographics
    display_fan_demographics(filtered_df)

    # Display filtered data
    st.write(filtered_df)
