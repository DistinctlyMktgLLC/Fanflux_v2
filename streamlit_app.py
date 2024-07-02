import streamlit as st
import pandas as pd
import folium
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import asyncio

# Set page configuration
st.set_page_config(page_title="Fanflux Intensity Finder", page_icon="🏆", layout="wide")

# Custom CSS to remove row lines from the table and style the sidebar
st.markdown(
    """
    <style>
    .dataframe th, .dataframe td {
        border: none !important;
    }
    .stSidebar {
        background-color: #f0f0f0;
        padding: 1rem;
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
    make, and their team and league preferences. Just click on the widgets below to explore!
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
    intensity_data["Fandom Level"] = intensity_data["Fandom Level"].astype(str)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar for filters with collapsible sections
st.sidebar.header("Filters")

with st.sidebar.expander("Teams"):
    teams = st.multiselect(
        "Select Teams",
        intensity_data['Team'].unique(),
        []
    )

with st.sidebar.expander("Leagues"):
    leagues = st.multiselect(
        "Select Leagues",
        intensity_data['League'].unique(),
        []
    )

with st.sidebar.expander("Race"):
    races = st.multiselect(
        "Select Race",
        intensity_data['Race'].unique(),
        []
    )

with st.sidebar.expander("Fandom Level"):
    fandom_levels = st.multiselect(
        "Select Fandom Level",
        intensity_data['Fandom Level'].unique(),
        []
    )

with st.sidebar.expander("Income Level"):
    income_levels = st.multiselect(
        "Select Income Level",
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
            f"# of Fans: {row[income_columns].sum()}"
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
    'Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race'
] + income_columns
# Adding pagination to the table
page_size = 50
total_rows = len(df_filtered)
current_page = st.sidebar.number_input('Page', min_value=1, max_value=(total_rows // page_size) + 1, step=1)

start_index = (current_page - 1) * page_size
end_index = start_index + page_size
df_paginated = df_filtered.iloc[start_index:end_index]

st.dataframe(df_paginated[columns_to_display].reset_index(drop=True))  # Reset index to remove row numbers

# Add collapsible sidebar
if st.sidebar.button('Toggle Sidebar'):
    st.session_state.sidebar_state = not st.session_state.sidebar_state

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = True

st.sidebar.empty()

if st.session_state.sidebar_state:
    st.sidebar.markdown(
        """
        <style>
        .stSidebar {
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        """
        <style>
        .stSidebar {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
