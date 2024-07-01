import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, MeasureControl, MousePosition

# Set page configuration
st.set_page_config(page_title="Fanflux Intensity Finder", page_icon="🏆", layout="wide")

# Custom CSS to remove row lines from the table
st.markdown(
    """
    <style>
    .dataframe th, .dataframe td {
        border: none !important;
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
    intensity_data.rename(columns={"Dispersion Score": "Intensity Score"}, inplace=True)
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

intensity = st.sidebar.slider("Intensity", 0, 100, (0, 100))

# Filter data based on widget input
@st.cache_data
def filter_data(data, teams, leagues, races, intensity_range):
    filtered_data = data[
        (data["Intensity Score"].between(intensity_range[0], intensity_range[1]))
    ]
    if teams:
        filtered_data = filtered_data[filtered_data["Team"].isin(teams)]
    if leagues:
        filtered_data = filtered_data[filtered_data["League"].isin(leagues)]
    if races:
        filtered_data = filtered_data[filtered_data["Race"].isin(races)]
    return filtered_data

try:
    df_filtered = filter_data(intensity_data, teams, leagues, races, intensity)
except Exception as e:
    st.error(f"Error filtering data: {e}")
    st.stop()

# Add interactive map using folium with MarkerCluster and additional details
try:
    if not df_filtered.empty:
        m = folium.Map(location=[df_filtered['US lat'].mean(), df_filtered['US lon'].mean()], zoom_start=5)

        # Add layer control with attribution
        folium.TileLayer('openstreetmap', name='OpenStreetMap', attr='© OpenStreetMap contributors').add_to(m)
        folium.TileLayer('cartodbpositron', name='CartoDB Positron', attr='© OpenStreetMap contributors, © CartoDB').add_to(m)
        folium.TileLayer('cartodbdark_matter', name='CartoDB Dark Matter', attr='© OpenStreetMap contributors, © CartoDB').add_to(m)
        folium.LayerControl().add_to(m)

        # Add marker cluster
        marker_cluster = MarkerCluster().add_to(m)
        for _, row in df_filtered.iterrows():
            try:
                tooltip_text = (
                    f"Neighborhood: {row['Neighborhood']}<br>"
                    f"Race: {row['Race']}<br>"
                    f"Team: {row['Team']}<br>"
                    f"League: {row['League']}<br>"
                    f"Income Level: {row['helper']}<br>"
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
            except KeyError as e:
                st.warning(f"Missing key {e} in row {row.name}")

        # Add measure control
        m.add_child(MeasureControl())

        # Add mouse position
        formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        mouse_position = MousePosition(
            position='topright',
            separator=' Long: ',
            empty_string='NaN',
            lng_first=True,
            num_digits=20,
            prefix='Coordinates:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        )
        m.add_child(mouse_position)

        st.write("## Map")
        st_folium(m, width=700, height=450)
    else:
        st.write("## Map")
        st.write("No data available for the selected filters.")
except Exception as e:
    st.error(f"Error creating map: {e}")
