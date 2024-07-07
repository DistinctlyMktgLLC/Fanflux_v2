# Pages/mlb_white.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load your data
df = pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")

# Colors for each fandom level
colors = {
    "Avid": "red",
    "Casual": "blue",
    "Convertible": "green"
}

def app():
    st.title("White Baseball Fans Analysis")
    st.header("Fan Demographics")

    # Calculate metrics
    total_avid_fans = df[df['Fandom Level'] == 'Avid']['Total Fans'].sum()
    total_casual_fans = df[df['Fandom Level'] == 'Casual']['Total Fans'].sum()
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible']['Total Fans'].sum()

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
        popup_content = f"Team: {row['Team']}<br>League: {row['League']}<br>Neighborhood: {row['Neighborhood']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}<br>Total Fans: {row['Total Fans']}"
        color = colors.get(row['Fandom Level'], 'black')
        folium.CircleMarker(
            location=[row['US lat'], row['US lon']],
            radius=5,
            popup=popup_content,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(folium_map)

    folium_static(folium_map)
