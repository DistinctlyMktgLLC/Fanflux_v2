import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium
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
    }
    .card-container {
        display: flex;
        justify-content: space-around;
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
race_counts = df_filtered["Race"].value_counts()

# Display metric cards using Streamlit's built-in functionality
st.write("## Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card"><h3>Average Intensity Score</h3><p>' + f"{average_intensity:.2f}" + '</p></div>', unsafe_allow_html=True)

for i, race in enumerate(races):
    with [col2, col3, col4][i % 3]:
        st.markdown(f'<div class="card"><h3>Number of {race} fans</h3><p>{race_counts.get(race, 0)}</p></div>', unsafe_allow_html=True)

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

# Add interactive map using folium
if not df_filtered.empty:
    m = folium.Map(location=[df_filtered['US lat'].mean(), df_filtered['US lon'].mean()], zoom_start=11)
    for _, row in df_filtered.iterrows():
        folium.CircleMarker(
            location=[row['US lat'], row['US lon']],
            radius=5,
            popup=f"{row['Team']} ({row['League']})",
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)
    st.write("## Map")
    st_folium(m, width=700, height=450)
else:
    st.write("## Map")
    st.write("No data available for the selected filters.")
