import streamlit as st
import pandas as pd

# Load data from Parquet file
@st.cache_data
def load_data():
    return pd.read_parquet('data/Fanflux_Intensity_MLB_AAPI.parquet')

def app():
    df = load_data()

    # Sidebar filters
    teams = df['Team'].unique().tolist()
    leagues = df['League'].unique().tolist()
    zipcodes = df['zipcode'].unique().tolist()

    selected_team = st.sidebar.selectbox("Select a Team", ["All"] + teams)
    selected_league = st.sidebar.selectbox("Select a League", ["All"] + leagues)
    selected_zipcode = st.sidebar.selectbox("Select a Zipcode", ["All"] + zipcodes)

    # Apply filters
    if selected_team != "All":
        df = df[df['Team'] == selected_team]
    if selected_league != "All":
        df = df[df['League'] == selected_league]
    if selected_zipcode != "All":
        df = df[df['zipcode'] == selected_zipcode]

    # Display data
    st.title("MLB AAPI Fans")
    st.dataframe(df[['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race',
                     'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
                     'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
                     'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
                     'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
                     'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
                     'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
                     'Wealthy ($100,000 to $149,999)', 'Rich ($150,000 or more)']])
