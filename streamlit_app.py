import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
from st_aggrid import AgGrid

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
st.metric(label="Average Intensity Score", value=f"{average_intensity:.2f}")

# Race count cards
for race in races:
    st.metric(label=f"Number of {race} fans", value=race_counts.get(race, 0))

# Filter out unwanted columns
columns_to_display = [col for col in df_filtered.columns if col not in ["dCategory", "US lat", "US lon", "helper"]]
df_filtered = df_filtered[columns_to_display]

# Display the filtered data as a table using ag-Grid
st.write("## Filtered Data Table")
AgGrid(df_filtered)

# Display the data as an Altair chart
chart = (
    alt.Chart(df_filtered)
    .mark_bar()
    .encode(
        x=alt.X("Team:N", title="Team"),
        y=alt.Y("Dispersion Score:Q", title="Intensity Score"),
        color="Race:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)

# Add interactive map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=df_filtered['US lat'].mean(),
        longitude=df_filtered['US lon'].mean(),
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_filtered,
            get_position='[US lon, US lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
            pickable=True,
        ),
    ],
    tooltip={"text": "{Team}\n{League}"}
))
