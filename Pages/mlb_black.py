import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

st.set_page_config(page_title="MLB Black Fans", page_icon="⚾️", layout="wide")

# Load data from Parquet file
@st.cache_data
def load_data():
    return pd.read_parquet('data/Fanflux_Intensity_MLB_Black.parquet')

df = load_data()

def app():
    st.title("MLB Black Fans")
    st.sidebar.header("Filter Data")

    teams = st.sidebar.multiselect("Select Team(s)", options=df['Team'].unique())
    leagues = st.sidebar.multiselect("Select League(s)", options=df['League'].unique())

    if teams:
        df_filtered = df[df['Team'].isin(teams)]
    if leagues:
        df_filtered = df[df['League'].isin(leagues)]
    if not teams and not leagues:
        df_filtered = df

    st.map(df_filtered)
    st.dataframe(df_filtered[['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race', 'Income']])

