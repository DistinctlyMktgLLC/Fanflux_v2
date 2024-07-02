import streamlit as st
import pandas as pd
import folium
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Set page configuration
st.set_page_config(page_title="Fanflux Intensity Finder", page_icon="🏆", layout="wide")

# Custom CSS to remove row lines from the table
st.markdown(
    """
    <style>
    .dataframe th, .dataframe td {
        border: none !important;
    }
    .stButton>button {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Show the page title and description
st.title("🏆 Find Fans")
st.write(
    """
    Fanflux visualizes Fan data from our Database that shows where fans live, how much they 
    make and their team and league preferences. Just click on the widgets below to explore!
    """
)

# Define income columns globally
income_columns = [
    'Struggling (Less than $10,000)',
    'Getting By ($10,000 to $14,999)',
    'Getting By ($15,000 to $19,999)',
    'Starting Out ($20,000 to $24,999)',
    'Starting Out ($25,000 to $29,999)',
    'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)',
    'Middle Class ($40,000 to $44,999)',
    'Middle Class ($45,000 to $49,999)',
    'Comfortable ($50,000 to $59,999)',
    'Comfortable ($60,000 to $74,999)',
    'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)',
    'Prosperous ($125,000 to $149,999)',
    'Wealthy ($150,000 to $199,999)',
    'Affluent ($200,000 or more)'
]

# Load data from Parquet files
@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

# Try loading the data and display basic information
try:
    intensity_data = load_data('data/Intensity_MLB_ALLRaces.parquet')
    intensity_data["zipcode"] = intensity_data["zipcode"].astype(str).str.zfill(5)
    # Ensure Fandom Level is in the correct format
    intensity_data["Fandom Level"] = intensity_data["Fandom Level"].astype(str)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar for filters
st.sidebar.header("Filters")
teams = st.sidebar.multiselect(
    "Teams",
    intensity_data['Team'].unique(),
    []
)

leagues = st.sidebar.multiselect(
    "Leagues",
    intensity_data['League'].unique(),
    []
)

races = st.sidebar.multiselect(
    "Race",
    intensity_data['Race'].unique(),
    []
)

fandom_levels = st.sidebar.multiselect(
    "Fandom Level",
    intensity_data['Fandom Level'].unique(),
    []
)

income_levels = st.sidebar.multiselect(
    "Income Level",
    income_columns,
    []
)

# Filter data based on widget input
@st.cache_data
def filter_data(data, teams, leagues, races, fandom_levels, income_levels):
    filtered_data = data.copy()
    if teams:
        filtered_data = filtered_data[filtered_data["Team"].isin(teams)]
    if leagues:
        filtered_data = filtered_data[filtered_data["League"].isin(leagues)]
    if races:
        filtered_data = filtered_data[filtered_data["Race"].isin(races)]
    if fandom_levels:
        filtered_data = filtered_data[filtered_data["Fandom Level"].isin(fandom_levels)]
    if income_levels:
        filtered_data = filtered_data.loc[:, income_columns + ['US lat', 'US lon', 'Neighborhood', 'Race', 'Team', 'League']]
        filtered_data['Total Fans'] = filtered_data[income_levels].sum(axis=1)
    return filtered_data

try:
    df_filtered = filter_data(intensity_data, teams, leagues, races, fandom_levels, income_levels)
except Exception as e:
    st.error(f"Error filtering data: {e}")
    st.stop()

# Show the map using leafmap
st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)

    # Add markers from filtered data
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df_filtered.iterrows():
        tooltip_text = (
            f"Neighborhood: {row['Neighborhood']}<br>"
            f"Race: {row['Race']}<br>"
            f"Team: {row['Team']}<br>"
            f"League: {row['League']}<br>"
            f"Fandom Level: {row['Fandom Level']}<br>"
            f"# of Fans: {row['Total Fans']}"
        )
        folium.CircleMarker(
            location=[row['US lat'], row['US lon']],
            radius=5,
            popup=tooltip_text,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(marker_cluster)

    m.to_streamlit(height=700)

# Optional: If you want to add a table as well
st.write("## Filtered Data Table")
columns_to_display = [
    'Team', 'League', 'Neighborhood', 'zipcode', 'Intensity',
    'Fandom Level', 'Race', 'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
    'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
    'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
    'Affluent ($200,000 or more)'
]

st.dataframe(df_filtered[columns_to_display].reset_index(drop=True))
