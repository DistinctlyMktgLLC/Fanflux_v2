import streamlit as st
from utils import load_data, filter_data, display_fan_demographics

def app():
    st.title("Fanflux League Analysis")

    # Load data
    df = load_data()
    
    if df.empty:
        st.error("Failed to load data.")
        st.stop()  # Stop execution if there are errors in loading data

    # Debug statement to print out the columns
    st.write("Columns in the dataset:", df.columns)
    
    # Ensure necessary columns are present
    required_columns = [
        'Avid Fans', 'Casual Fans', 'Convertible Fans', 'League', 'Team', 'Race', 'Fandom Level',
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 
        'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)', 
        'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)', 
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 
        'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)', 
        'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)', 
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 
        'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"The following required columns are missing in the dataset: {', '.join(missing_columns)}")
        st.stop()

    # Multiselect filters
    leagues = st.multiselect("Select Leagues", options=df['League'].unique())
    teams = st.multiselect("Select Teams", options=df['Team'].unique())
    fandom_levels = st.multiselect("Select Fandom Levels", options=df['Fandom Level'].unique())
    races = st.multiselect("Select Races", options=df['Race'].unique())
    income_levels = st.multiselect(
        "Select Income Levels", 
        options=[
            'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 
            'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)', 
            'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)', 
            'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 
            'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)', 
            'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)', 
            'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 
            'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
        ]
    )

    # Filter data based on selections
    filtered_df = filter_data(df, leagues, teams, fandom_levels, races, income_levels)

    # Display fan demographics
    display_fan_demographics(filtered_df)

    # Display filtered data
    st.write(filtered_df)

