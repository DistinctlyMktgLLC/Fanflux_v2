import streamlit as st
import pandas as pd
import folium
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

def load_data(file_path):
    return pd.read_parquet(file_path)

def app():
    st.title("MLB Asian Fan Data")

    # Load data
    data_path = 'data/Fanflux_Intensity_MLB_Asian.parquet'
    data = load_data(data_path)

    # Sidebar for filters
    st.sidebar.header("Filters")
    teams = st.sidebar.multiselect("Teams", data['Team'].unique(), [])
    leagues = st.sidebar.multiselect("Leagues", data['League'].unique(), [])
    races = st.sidebar.multiselect("Race", data['Race'].unique(), [])
    fandom_levels = st.sidebar.multiselect("Fandom Level", data['Fandom Level'].unique(), [])

    # Filter data
    filtered_data = data[
        (data["Team"].isin(teams) if teams else True) &
        (data["League"].isin(leagues) if leagues else True) &
        (data["Race"].isin(races) if races else True) &
        (data["Fandom Level"].isin(fandom_levels) if fandom_levels else True)
    ]

    # Display map
    m = leafmap.Map(center=(filtered_data['US lat'].mean(), filtered_data['US lon'].mean()), zoom=5)
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['US lat'], row['US lon']],
            popup=(
                f"Neighborhood: {row['Neighborhood']}<br>"
                f"Race: {row['Race']}<br>"
                f"Team: {row['Team']}<br>"
                f"League: {row['League']}<br>"
                f"Fandom Level: {row['Fandom Level']}<br>"
                f"# of Fans: {row[['Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
                                  'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
                                  'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
                                  'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
                                  'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
                                  'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
                                  'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
                                  'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)']].sum()}"
            ),
        ).add_to(marker_cluster)
    
    st_folium(m, width=700, height=500)

    # Display filtered data
    st.write("## Filtered Data Table")
    st.dataframe(filtered_data)

if __name__ == "__main__":
    app()
