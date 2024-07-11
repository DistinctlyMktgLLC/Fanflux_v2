import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Main app function for leagues analysis
def app():
    st.title("Leagues Analysis")

    # Filters
    st.sidebar.header("Filters")
    selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", ["Avid", "Casual", "Convertible"], key="fandom_level_filter_unique_1")
    selected_races = st.sidebar.multiselect("Select Race", ["Black", "Hispanic", "White", "Asian", "Other"], key="race_filter_unique_1")
    selected_leagues = st.sidebar.multiselect("Select League", ["NFL", "NBA", "MLB", "NHL", "MLS"], key="league_filter_unique_1")
    selected_teams = st.sidebar.multiselect("Select Team", ["Minnesota Twins", "Cincinnati Reds", "Houston Astros"], key="team_filter_unique_1")
    selected_income_levels = st.sidebar.multiselect("Select Income Level", [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
        'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
        'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
        'Affluent ($200,000 or more)'
    ], key="income_level_filter_unique_1")

    # Simulated filtered data
    filtered_df = pd.DataFrame({
        'Fandom Level': ['Avid', 'Casual', 'Convertible'],
        'Race': ['Black', 'Hispanic', 'White'],
        'League': ['NFL', 'NBA', 'MLB'],
        'Team': ['Minnesota Twins', 'Cincinnati Reds', 'Houston Astros'],
        'Struggling (Less than $10,000)': [10000, 20000, 15000],
        'Getting By ($10,000 to $14,999)': [5000, 7000, 8000],
        'Middle Class ($35,000 to $39,999)': [35000, 39000, 37000]
    })

    # Apply filters
    if selected_fandom_levels:
        filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom_levels)]
    if selected_races:
        filtered_df = filtered_df[filtered_df['Race'].isin(selected_races)]
    if selected_leagues:
        filtered_df = filtered_df[filtered_df['League'].isin(selected_leagues)]
    if selected_teams:
        filtered_df = filtered_df[filtered_df['Team'].isin(selected_teams)]
    if selected_income_levels:
        filtered_df = filtered_df[(filtered_df[selected_income_levels].sum(axis=1) > 0)]

    # Calculate metrics
    income_columns = [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
        'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
        'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
        'Affluent ($200,000 or more)'
    ]

    total_avid_fans = filtered_df[filtered_df['Fandom Level'] == 'Avid'][income_columns].sum().sum()
    total_casual_fans = filtered_df[filtered_df['Fandom Level'] == 'Casual'][income_columns].sum().sum()
    total_convertible_fans = filtered_df[filtered_df['Fandom Level'] == 'Convertible'][income_columns].sum().sum()

    # Display metrics in scorecards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Avid Fans", value=int(total_avid_fans), key="avid_metric_unique_1")
    with col2:
        st.metric(label="Total Casual Fans", value=int(total_casual_fans), key="casual_metric_unique_1")
    with col3:
        st.metric(label="Total Convertible Fans", value=int(total_convertible_fans), key="convertible_metric_unique_1")

    # Display map
    st.header("Fan Opportunity Map")
    folium_map = folium.Map(location=[37.7749, -122.4194], zoom_start=4)

    for i, row in filtered_df.iterrows():
        folium.CircleMarker(
            location=[37.7749 + i, -122.4194 + i],  # Sample locations
            radius=5,
            popup=f"Team: {row['Team']}<br>League: {row['League']}<br>Race: {row['Race']}<br>Total Fans: {row[income_columns].sum()}",
            color='red' if row['Fandom Level'] == 'Avid' else 'blue' if row['Fandom Level'] == 'Casual' else 'green',
            fill=True,
            fill_color='red' if row['Fandom Level'] == 'Avid' else 'blue' if row['Fandom Level'] == 'Casual' else 'green'
        ).add_to(folium_map)

    folium_static(folium_map, width=1200, height=800)

# Ensure the app function is only called if this script is run directly
if __name__ == "__main__":
    app()
