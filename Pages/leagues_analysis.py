import streamlit as st
import polars as pl
import folium
from streamlit_folium import folium_static

# Load the updated data
@st.cache_data
def load_data():
    df = pl.read_parquet('data/updated_combined_leagues.parquet')
    return df

df = load_data()

def app():
    st.title("Leagues Analysis")

    # Filters
    st.sidebar.header("Filters")
    selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique(), key="fandom_level_filter_leagues")
    selected_races = st.sidebar.multiselect("Select Race", df['Race'].unique(), key="race_filter_leagues")
    selected_leagues = st.sidebar.multiselect("Select League", df['League'].unique(), key="league_filter_leagues")
    selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique(), key="team_filter_leagues")
    selected_income_levels = st.sidebar.multiselect("Select Income Level", df.columns[12:], key="income_level_filter_leagues")

    # Apply filters
    filtered_df = df
    if selected_fandom_levels:
        filtered_df = filtered_df.filter(pl.col('Fandom Level').is_in(selected_fandom_levels))
    if selected_races:
        filtered_df = filtered_df.filter(pl.col('Race').is_in(selected_races))
    if selected_leagues:
        filtered_df = filtered_df.filter(pl.col('League').is_in(selected_leagues))
    if selected_teams:
        filtered_df = filtered_df.filter(pl.col('Team').is_in(selected_teams))
    if selected_income_levels:
        filtered_df = filtered_df.filter(filtered_df[selected_income_levels].sum(axis=1) > 0)

    # Convert to Pandas for rendering
    filtered_df = filtered_df.to_pandas()

    # Calculate metrics
    total_avid_fans = filtered_df[filtered_df['Fandom Level'] == 'Avid']['Total Fans'].sum()
    total_casual_fans = filtered_df[filtered_df['Fandom Level'] == 'Casual']['Total Fans'].sum()
    total_convertible_fans = filtered_df[filtered_df['Fandom Level'] == 'Convertible']['Total Fans'].sum()

    # Display metrics in scorecards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Avid Fans", value=int(total_avid_fans))
    with col2:
        st.metric(label="Total Casual Fans", value=int(total_casual_fans))
    with col3:
        st.metric(label="Total Convertible Fans", value=int(total_convertible_fans))

    # Create the map with marker clustering
    st.subheader("Fan Opportunity Map")
    with st.spinner("Finding Fandom..."):
        m = folium.Map(location=[40, -100], zoom_start=4)
        marker_cluster = folium.plugins.MarkerCluster().add_to(m)

        for _, row in filtered_df.iterrows():
            folium.Marker(
                location=[row["US lat"], row["US lon"]],
                popup=f"Team: {row['Team']}<br>League: {row['League']}<br>Neighborhood: {row['Neighborhood']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}<br>Total Fans: {row['Total Fans']}",
                icon=folium.Icon(color={"Avid": "red", "Casual": "blue", "Convertible": "green"}[row["Fandom Level"]])
            ).add_to(marker_cluster)

        folium_static(m, width=1200, height=700)

# Run the app function
if __name__ == "__main__":
    app()
