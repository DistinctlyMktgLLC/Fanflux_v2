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

def app():
    st.title("White Baseball Fans Analysis")
    st.header("Fan Demographics")

    # Calculate metrics
    total_avid_fans = df[df['Fandom Level'] == 'Avid']['Intensity'].sum()
    total_casual_fans = df[df['Fandom Level'] == 'Casual']['Intensity'].sum()
    total_convertible_fans = df[income_columns].sum().sum()

    # Display metrics in scorecards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Avid Fans", value=int(total_avid_fans))
    with col2:
        st.metric(label="Total Casual Fans", value=int(total_casual_fans))
    with col3:
        st.metric(label="Total Convertible Fans", value=int(total_convertible_fans))

    st.header("Fan Opportunity Map")

    # Create a map
    folium_map = folium.Map(location=[37.7749, -122.4194], zoom_start=4, control_scale=True)

    for _, row in df.iterrows():
        popup_content = f"Team: {row['Team']}<br>League: {row['League']}<br>Neighborhood: {row['Neighborhood']}<br>Fandom Level: {row['Fandom Level']}<br>Race: {row['Race']}<br>Total Fans: {row[income_columns].sum()}"
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

    # Custom CSS for full width map
    st.markdown(
        """
        <style>
        .folium-map {
            width: 100% !important;
            height: 600px !important;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

# Run the app
if __name__ == "__main__":
    app()
