import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

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

# Show multiselect widget for fan types
fan_types = st.multiselect(
    "Fan Types",
    intensity_data['fan_type'].unique(),
    ["avid", "casual", "not at all"],
)

# Show slider widget for intensity
intensity = st.slider("Intensity", 0, 100, (0, 100))

# Filter data based on widget input
df_filtered = intensity_data[
    (intensity_data["fan_type"].isin(fan_types)) & 
    (intensity_data["intensity_score"].between(intensity[0], intensity[1]))
]

# Display the filtered data as a table
st.dataframe(df_filtered)

# Display the data as an Altair chart
chart = (
    alt.Chart(df_filtered)
    .mark_bar()
    .encode(
        x=alt.X("team:N", title="Team"),
        y=alt.Y("intensity_score:Q", title="Intensity Score"),
        color="fan_type:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)

# Add interactive map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=df_filtered['latitude'].mean(),
        longitude=df_filtered['longitude'].mean(),
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_filtered,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
            pickable=True,
        ),
    ],
    tooltip={"text": "{team}\n{league}"}
))
