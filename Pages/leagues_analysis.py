import streamlit as st
import folium
from streamlit_folium import folium_static
import polars as pl

@st.cache_data
def load_data():
    df = pl.read_parquet('data/updated_combined_leagues.parquet')
    return df

df = load_data().to_pandas()

def app():
    st.title("Leagues Analysis")

    st.sidebar.header("Filters")
    selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique(), key="fandom_level_filter_leagues")
    selected_races = st.sidebar.multiselect("Select Race", df['Race'].unique(), key="race_filter_leagues")
    selected_leagues = st.sidebar.multiselect("Select League", df['League'].unique(), key="league_filter_leagues")
    selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique(), key="team_filter_leagues")
    selected_income_levels = st.sidebar.multiselect("Select Income Level", df.columns[12:], key="income_level_filter_leagues")

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

    total_avid_fans = filtered_df[filtered_df['Fandom Level'] == 'Avid']['Total Fans'].sum()
    total_casual_fans = filtered_df[filtered_df['Fandom Level'] == 'Casual']['Total Fans'].sum()
    total_convertible_fans = filtered_df[filtered_df['Fandom Level'] == 'Convertible']['Total Fans'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Avid Fans", value=int(total_avid_fans))
    with col2:
        st.metric(label="Total Casual Fans", value=int(total_casual_fans))
    with col3:
        st.metric(label="Total Convertible Fans", value=int(total_convertible_fans))

    st.subheader("Fan Opportunity Map")
    with st.spinner("Finding Fandom..."):
        m = folium.Map(location=[40, -100], zoom_start=4)

        for _, row in filtered_df.iterrows():
            folium.CircleMarker(
                location=[row["US lat"], row["US lon"]],
                radius=5,
                color={"Avid": "red", "Casual": "blue", "Convertible": "green"}[row["Fandom Level"]],
                fill=True,
                popup=f"Team: {row['Team']}<br>League: {row['League']}<br>Neighborhood: {row['Neighborhood']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}<br>Total Fans: {row['Total Fans']}"
            ).add_to(m)

        folium_static(m, width=1200, height=700)
