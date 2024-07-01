import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

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

# Try loading the data and display basic information
try:
    intensity_data = load_data('data/Intensity_MLB_ALLRaces.csv')
    intensity_data["zipcode"] = intensity_data["zipcode"].astype(str).str.zfill(5)
    intensity_data.rename(columns={"Dispersion Score": "Intensity Score"}, inplace=True)
except Exception as e:
    st.error(f"Error loading data: {e}")

# Show multiselect widget for teams with no default selections
teams = st.multiselect(
    "Teams",
    intensity_data['Team'].unique(),
    []
)

# Show multiselect widget for leagues with no default selections
leagues = st.multiselect(
    "Leagues",
    intensity_data['League'].unique(),
    []
)

# Show multiselect widget for races with no default selections
races = st.multiselect(
    "Race",
    intensity_data['Race'].unique(),
    []
)

# Show slider widget for intensity
intensity = st.slider("Intensity", 0, 100, (0, 100))

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

# Display the filtered data as a table using st.table
st.write("## Fan Insights")
st.table(df_filtered)

# Add interactive map using folium with basic markers
try:
    if not df_filtered.empty:
        m = folium.Map(location=[df_filtered['US lat'].mean(), df_filtered['US lon'].mean()], zoom_start=5)

        for _, row in df_filtered.iterrows():
            tooltip_text = (
                f"Neighborhood: {row['Neighborhood']}<br>"
                f"Race: {row['Race']}<br>"
                f"Team: {row['Team']}<br>"
                f"League: {row['League']}<br>"
                f"Income Level: {row['helper']}<br>"
                f"# of Fans: {row[income_columns].sum()}"
            )
            folium.Marker(
                location=[row['US lat'], row['US lon']],
                popup=tooltip_text,
                tooltip=tooltip_text
            ).add_to(m)

        st.write("## Map")
        st_folium(m, width=700, height=450)
    else:
        st.write("## Map")
        st.write("No data available for the selected filters.")
except Exception as e:
    st.error(f"Error creating map: {e}")
