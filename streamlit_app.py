import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from st_aggrid import AgGrid

# Set page configuration
st.set_page_config(page_title="Fanflux Intensity Finder", page_icon="🏆")

# Custom CSS for scorecards
st.markdown(
    """
    <style>
    .card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        flex: 1;
        font-size: 16px;
    }
    .card-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
    }
    .card h3 {
        font-size: 18px;
        margin: 10px 0;
    }
    .card p {
        font-size: 24px;
        margin: 0;
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

# Load data from CSV files
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load the intensity data
intensity_data = load_data('data/Intensity_MLB_ALLRaces.csv')

# Identify income level columns
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
df_filtered = intensity_data[
    (intensity_data["Team"].isin(teams)) & 
    (intensity_data["League"].isin(leagues)) &
    (intensity_data["Race"].isin(races)) &
    (intensity_data["Dispersion Score"].between(intensity[0], intensity[1]))
]

# Calculate metrics
average_intensity = df_filtered["Dispersion Score"].mean()

# Calculate total number of people for each race
race_totals = {}
for race in races:
    race_data = df_filtered[df_filtered["Race"] == race]
    total_people = race_data[income_columns].sum().sum()
    race_totals[race] = total_people

# Display metric cards using custom styling
st.write("## Metrics")
st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.markdown(f'<div class="card"><h3>Average Intensity Score</h3><p>{average_intensity:.2f}</p></div>', unsafe_allow_html=True)
for race, total in race_totals.items():
    st.markdown(f'<div class="card"><h3>Number of {race} fans</h3><p>{total}</p></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Filter out unwanted columns for display table but keep for map
columns_to_hide = ["dCategory", "helper"]
columns_to_display = [col for col in df_filtered.columns if col not in columns_to_hide and not col.startswith("Unnamed")]
df_display = df_filtered[columns_to_display]

# Display the filtered data as a table using ag-Grid
st.write("## Filtered Data Table")
AgGrid(df_display)

# Display the data as an Altair chart
chart = (
    alt.Chart(df_display)
    .mark_bar()
    .encode(
        x=alt.X("Team:N", title="Team"),
        y=alt.Y("Dispersion Score:Q", title="Intensity Score"),
        color="Race:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)

# Add interactive map using folium with MarkerCluster
if not df_filtered.empty:
    m = folium.Map(location=[df_filtered['US lat'].mean(), df_filtered['US lon'].mean()], zoom_start=11)
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df_filtered.iterrows():
        tooltip_text = (
            f"Neighborhood: {row['Neighborhood']}<br>"
            f"Race: {row['Race']}<br>"
            f"Team: {row['Team']}<br>"
            f"League: {row['League']}<br>"
            f"Income Level: {row['helper']}<br>"  # Adjust this column name as needed
            f"# of Fans: {row[income_columns].sum()}"  # Adjust this to sum the number of fans
        )
        folium.CircleMarker(
            location=[row['US lat'], row['US lon']],
            radius=5,
            popup=tooltip_text,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(marker_cluster)
    st.write("## Map")
    st_folium(m, width=700, height=450)
else:
    st.write("## Map")
    st.write("No data available for the selected filters.")
