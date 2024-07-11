import streamlit as st
import polars as pl
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Load the data
@st.cache_data
def load_data():
    return pl.read_parquet('data/combined_leagues.parquet')

df = load_data().to_pandas()

# Main app function for leagues analysis
def app():
    st.title("Leagues Analysis")

    # Filters
    st.sidebar.header("Filters")
    selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique(), key="fandom_level_filter_unique")
    selected_races = st.sidebar.multiselect("Select Race", df['Race'].unique(), key="race_filter_unique")
    selected_leagues = st.sidebar.multiselect("Select League", df['League'].unique(), key="league_filter_unique")
    selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique(), key="team_filter_unique")
    selected_income_levels = st.sidebar.multiselect("Select Income Level", df.columns[12:], key="income_level_filter_unique")

    # Apply filters
    filtered_df = df.copy()
    if selected_fandom_levels:
        filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom_levels)]
    if selected_races:
        filtered_df = filtered_df[filtered_df['Race'].isin(selected_races)]
    if selected_leagues:
        filtered_df = filtered_df[filtered_df['League'].isin(selected_leagues)]
    if selected_teams:
        filtered_df = filtered_df[filtered_df['Team'].isin(selected_teams)]
    if selected_income_levels:
        filtered_df = filtered_df[selected_income_levels + ['US lat', 'US lon']]

    # Calculate metrics
    total_avid_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Avid'])
    total_casual_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Casual'])
    total_convertible_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Convertible'])

    st.metric(label="Total Avid Fans", value=total_avid_fans)
    st.metric(label="Total Casual Fans", value=total_casual_fans)
    st.metric(label="Total Convertible Fans", value=total_convertible_fans)

    # Create the map
    st.text("Finding Fandom...")
    folium_map = folium.Map(location=[37.7749, -122.4194], zoom_start=4)
    marker_cluster = MarkerCluster().add_to(folium_map)

    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['US lat'], row['US lon']],
            popup=f"Team: {row['Team']}<br>League: {row['League']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}",
            icon=folium.Icon(color='red' if row['Fandom Level'] == 'Avid' else 'blue' if row['Fandom Level'] == 'Casual' else 'green')
        ).add_to(marker_cluster)

    folium_static(folium_map, width=1200, height=800)

if __name__ == "__main__":
    app()
