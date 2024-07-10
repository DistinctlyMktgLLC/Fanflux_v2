import streamlit as st
from utils import load_data, display_fan_demographics, filter_data

def app():
    st.title("Fanflux League Analysis")

    df = load_data()

    leagues = st.multiselect("Select Leagues", options=df['League'].unique())
    teams = st.multiselect("Select Teams", options=df['Team'].unique())
    fandom_levels = st.multiselect("Select Fandom Levels", options=df['Fandom Level'].unique())
    races = st.multiselect("Select Races", options=df['Race'].unique())
    income_levels = st.multiselect("Select Income Levels", options=df['Income Level'].unique())

    filtered_df = filter_data(df, leagues, teams, fandom_levels, races, income_levels)

    display_fan_demographics(filtered_df)

    # Display the map
    st.map(filtered_df[['Latitude', 'Longitude']])
