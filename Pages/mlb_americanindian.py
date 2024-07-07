# Pages/mlb_aapi.py (similarly for other pages)
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Colors for each fandom level
colors = {
    "Avid": "red",
    "Casual": "blue",
    "Convertible": "green"
}

# List of income columns
income_columns = [
    'Struggling (Less than $10,000)',
    'Getting By ($10,000 to $14,999)',
    'Getting By ($15,000 to $19,999)',
    'Starting Out ($20,000 to $24,999)',
    'Starting Out ($25,000 to $29,999)',
    'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)',
    'Middle Class ($40,000 to $44,999)',
    'Middle Class ($45,000 to $49,999)',
    'Comfortable ($50,000 to $59,999)',
    'Comfortable ($60,000 to $74,999)',
    'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)',
    'Prosperous ($125,000 to $149,999)',
    'Wealthy ($150,000 to $199,999)',
    'Affluent ($200,000 or more)'
]

def app(filtered_df=None):
    st.title("American Indian Baseball Fans Analysis")
    st.header("Fan Demographics")

    # Use the filtered dataframe if provided, else use the full dataframe
    df = filtered_df if filtered_df is not None else pd.read_parquet("data/Fanflux_Intensity_MLB_AmericanIndian.parquet")

    # Calculate metrics
    total_avid_fans = df[df['Fandom Level'] == 'Avid']['Intensity'].sum()
    total_casual_fans = df[df['Fandom Level'] == 'Casual']['Intensity'].sum()
    total_convertible_fans = df[income_columns].sum().sum()

    # Display metrics in scorecards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Avid Fans", value=total_avid_fans, delta_color="off")
    with col2:
        st.metric(label="Total Casual Fans", value=total_casual_fans, delta_color="off")
    with col3:
        st.metric(label="Total Convertible Fans", value=total_convertible_fans, delta_color="off")

    st.header("Fan Opportunity Map")

    # Create a map
    folium_map = folium.Map(location=[37.7749, -122.4194], zoom_start=4)

    for _, row in df.iterrows():
        # Update popup content to use "Convertible" instead of "Not at All"
        popup_content = f"Team: {row['Team']}<br>League: {row['League']}<br>Neighborhood: {row['Neighborhood']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}<br>Intensity: {row['Intensity']}<br>Convertible Fans: {row[income_columns].sum()}"
        color = colors.get(row['Fandom Level'], 'black')
        folium.CircleMarker(
            location=[row['US lat'], row['US lon']],
            radius=5,
            popup=popup_content,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(folium_map)

    folium_static(folium_map, width=1200, height=800)
