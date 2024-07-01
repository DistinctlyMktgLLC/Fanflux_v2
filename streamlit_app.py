import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Fanflux Intensity Finder", page_icon="🏆")

# Show the page title and description
st.title("🏆 Find Fans")
st.write(
    """
    Fanflux visualizes Fan data from our Database that shows where fans live, how much they 
    make and their team and league preferences. Just click on the widgets below to explore!
    """
)

# Load data from CSV files
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Try loading the data and display basic information
try:
    intensity_data = load_data('data/Intensity_MLB_ALLRaces.csv')
    st.write("Data loaded successfully!")
    st.write(intensity_data.head())
except Exception as e:
    st.error(f"Error loading data: {e}")

# Show multiselect widget for teams
teams = st.multiselect(
    "Teams",
    intensity_data['Team'].unique(),
    intensity_data['Team'].unique()
)

# Show multiselect widget for leagues
leagues = st.multiselect(
    "Leagues",
    intensity_data['League'].unique(),
    intensity_data['League'].unique()
)

# Show multiselect widget for races
races = st.multiselect(
    "Race",
    intensity_data['Race'].unique(),
    intensity_data['Race'].unique()
)

# Show slider widget for intensity
intensity = st.slider("Intensity", 0, 100, (0, 100))

# Filter data based on widget input
@st.cache_data
def filter_data(data, teams, leagues, races, intensity_range):
    return data[
        (data["Team"].isin(teams)) & 
        (data["League"].isin(leagues)) &
        (data["Race"].isin(races)) &
        (data["Dispersion Score"].between(intensity_range[0], intensity_range[1]))
    ]

try:
    df_filtered = filter_data(intensity_data, teams, leagues, races, intensity)
    st.write("Data filtered successfully!")
    st.write(df_filtered.head())
except Exception as e:
    st.error(f"Error filtering data: {e}")
