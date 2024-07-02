import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium
from streamlit_folium import st_folium
from st_aggrid import AgGrid, GridOptionsBuilder

# Load data from Parquet file
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_parquet(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

def app():
    df = load_data('data/Fanflux_Intensity_MLB_AAPI.parquet')

    if df.empty:
        return

    # Sidebar filters
    teams = df['Team'].unique().tolist() if 'Team' in df.columns else []
    leagues = df['League'].unique().tolist() if 'League' in df.columns else []
    zipcodes = df['zipcode'].unique().tolist() if 'zipcode' in df.columns else []

    selected_team = st.sidebar.selectbox("Select a Team", ["All"] + teams)
    selected_league = st.sidebar.selectbox("Select a League", ["All"] + leagues)
    selected_zipcode = st.sidebar.selectbox("Select a Zipcode", ["All"] + zipcodes)

    # Apply filters
    if selected_team != "All" and 'Team' in df.columns:
        df = df[df['Team'] == selected_team]
    if selected_league != "All" and 'League' in df.columns:
        df = df[df['League'] == selected_league]
    if selected_zipcode != "All" and 'zipcode' in df.columns:
        df = df[df['zipcode'] == selected_zipcode]

    # Display data
    st.title("MLB AAPI Fans")

    # Ensure the necessary columns are in the dataframe before displaying
    columns_to_display = ['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race',
                          'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
                          'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
                          'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
                          'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
                          'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
                          'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
                          'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
                          'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)']
    
    existin
