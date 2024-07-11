import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Main app function for leagues analysis
def app(df):
    st.title("Leagues Analysis")

    # Filters
    st.sidebar.header("Filters")
    selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique(), key="fandom_level_filter_1")
    selected_races = st.sidebar.multiselect("Select Race", df['Race'].unique(), key="race_filter_1")
    selected_leagues = st.sidebar.multiselect("Select League", df['League'].unique(), key="league_filter_1")
    selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique(), key="team_filter_1")
    selected_income_levels = st.sidebar.multiselect("Select Income Level", df.columns[14:], key="income_level_filter_1")

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
        filtered_df = filtered_df[filtered_df[selected_income_levels].sum(axis=1) > 0]

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
        st.metric(label="Total Avid Fans", value=int(total_avid_fans))
    with col2:
        st.metric(label="Total Casual Fans", value=int(total_casual_fans))
    with col3:
        st.metric(label="Total Convertible Fans", value=int(total_convertible_fans))

    # Display map
    st.header("Fan Opportunity Map")
    folium_map = folium.Map(location=[37.7749, -122.4194], zoom_start=4)

    for _, row in filtered_df.iterrows():
        fandom_level = row['Fandom Level']
        popup_content = f"Team: {row['Team']}<br>League: {row['League']}<br>Neighborhood: {row['Neighborhood']}<br>Fandom Level: {fandom_level}<br>Race: {row['Race']}<br>Total Fans: {row[income_columns].sum()}"
        color = 'red' if fandom_level == 'Avid' else 'blue' if fandom_level == 'Casual' else 'green'
        folium.CircleMarker(
            location=[row['US lat'], row['US lon']],
            radius=5,
            popup=popup_content,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(folium_map)

    folium_static(folium_map, width=1200, height=800)
