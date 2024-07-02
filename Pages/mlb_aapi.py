def app():
    import streamlit as st
    import pandas as pd
    import folium
    from folium.plugins import MarkerCluster
    from streamlit_folium import st_folium

    # Set page configuration
    st.set_page_config(page_title="MLB AAPI Fans", page_icon="⚾", layout="wide")

    # Load data from Parquet file
    @st.cache_data
    def load_data():
        return pd.read_parquet('data/Fanflux_Intensity_MLB_AAPI.parquet')

    # Try loading the data and display basic information
    try:
        intensity_data = load_data()
        intensity_data["zipcode"] = intensity_data["zipcode"].astype(str).str.zfill(5)
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

    # Filter data based on widget input
    @st.cache_data
    def filter_data(data, teams, leagues, races, fandom_levels):
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
        df_filtered = filter_data(intensity_data, teams, leagues, races, fandom_levels)
    except Exception as e:
        st.error(f"Error filtering data: {e}")
        st.stop()

    # Show the map using folium
    st.title("Interactive Map of MLB AAPI Fans")

    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    # Add markers from filtered data
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df_filtered.iterrows():
        tooltip_text = (
            f"Neighborhood: {row['Neighborhood']}<br>"
            f"Race: {row['Race']}<br>"
            f"Team: {row['Team']}<br>"
            f"League: {row['League']}<br>"
            f"Fandom Level: {row['Fandom Level']}<br>"
            f"# of Fans: {row[['Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)', 'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)', 'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)']].sum()}"
        )
        folium.CircleMarker(
            location=[row['US lat'], row['US lon']],
            radius=5,
            popup=tooltip_text,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(marker_cluster)

    # Display the map in Streamlit
    st_folium(m, width=700, height=500)

    # Optional: If you want to add a table as well
    st.write("## Filtered Data Table")
    st.dataframe(df_filtered[['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race', 'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)', 'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)', 'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)']].reset_index(drop=True))
