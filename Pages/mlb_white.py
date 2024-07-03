import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
from utils import load_data, create_map, add_map_markers, apply_common_styles

def app():
    st.title("White Baseball Fans")

    df = load_data("data/Fanflux_Intensity_MLB_White.parquet")  # Adjust the file path accordingly

    if df.empty:
        st.error("No data available.")
        return

    # Filter options
    st.sidebar.header("Filters")
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    league = st.sidebar.selectbox('Select a League', ['Choose an option'] + sorted(df['League'].unique()))
    city = st.sidebar.selectbox('Select a City', ['Choose an option'] + sorted(df['City'].unique()))
    fandom_level = st.sidebar.selectbox('Select Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))
    income_levels = [col for col in df.columns if 'Income' in col]

    filtered_df = df.copy()
    if team != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Team'] == team]
    if league != 'Choose an option':
        filtered_df = filtered_df[filtered_df['League'] == league]
    if city != 'Choose an option':
        filtered_df = filtered_df[filtered_df['City'] == city]
    if fandom_level != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Fandom Level'] == fandom_level]

    # Ensure zipcode is formatted with leading zeros
    filtered_df['zipcode'] = filtered_df['zipcode'].apply(lambda x: f"{x:05d}")

    # Create Total Fans column
    filtered_df['Total Fans'] = filtered_df[income_levels].sum(axis=1)

    # Define columns to display
    columns_to_display = [
        'dCategory', 'Team', 'League', 'City', 'Neighborhood', 
        'zipcode', 'Intensity', 'Fandom Level', 'Race', 'Total Fans'
    ]

    # Display the table
    st.write("### Filtered Data")
    st.dataframe(
        filtered_df[columns_to_display],
        width=1200, 
        height=400
    )

    # Create the map
    st.write("### Fan Opportunity Map")
    m = create_map()
    color_key = {
        'Avid': 'red',
        'Casual': 'blue',
        'Convertible': 'green'
    }
    add_map_markers(m, filtered_df, 'Fandom Level', color_key)
    st_folium(m, width=700, height=500)

if __name__ == "__main__":
    app()
