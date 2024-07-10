import streamlit as st
import pandas as pd
from utils import load_data, filter_data, display_fan_demographics

def app():
    st.title("Fanflux League Analysis")
    
    df = load_data()

    leagues = st.multiselect("Select Leagues", options=df['League'].unique())
    teams = st.multiselect("Select Teams", options=df['Team'].unique())
    fandom_levels = st.multiselect("Select Fandom Levels", options=["Avid", "Casual", "Convertible"])
    races = st.multiselect("Select Races", options=df['Race'].unique())
    
    # Ensure the income columns exist in the DataFrame
    income_columns = [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 
        'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)', 
        'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)', 
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 
        'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)', 
        'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)', 
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 
        'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
    ]

    for col in income_columns:
        if col not in df.columns:
            st.error(f"The column '{col}' is missing in the dataset.")
            return

    income_levels = st.multiselect("Select Income Levels", options=income_columns)

    filtered_df = filter_data(df, leagues, teams, fandom_levels, races, income_levels)
    
    display_fan_demographics(filtered_df)

    # Display income levels totals
    if income_levels:
        total_income = filtered_df[income_levels].sum().sum()
        st.metric(label="Total Income Level Fans", value=total_income)
    else:
        total_income = df[income_columns].sum().sum()
        st.metric(label="Total Income Level Fans", value=total_income)
