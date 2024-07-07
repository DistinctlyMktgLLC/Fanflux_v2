# mlb_white.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Set the page config at the top
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Load your data
df = pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")

# Colors for each fandom level
colors = {
    'Avid': 'red',
    'Casual': 'blue',
    'Convertible': 'green'
}

# Define the income columns
income_columns = [col for col in df.columns if 'Income' in col]

# Calculate the total fans
total_avid_fans = df[df['Fandom Level'] == 'Avid'][income_columns].sum().sum()
total_casual_fans = df[df['Fandom Level'] == 'Casual'][income_columns].sum().sum()
total_convertible_fans = df[df['Fandom Level'] == 'Convertible'][income_columns].sum().sum()

# Display the scorecards with color coding and styling
st.markdown("""
<style>
    .scorecard {
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        background-color: black;
        color: white;
        font-size: 25px;
        text-align: center;
        font-family: 'Roboto Mono', monospace;
        position: relative;
    }
    .scorecard::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 10px;
        border-radius: 10px 0 0 10px;
    }
    .scorecard.avid::before {
        background-color: red;
    }
    .scorecard.casual::before {
        background-color: blue;
    }
    .scorecard.convertible::before {
        background-color: green;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="scorecard avid">Total Avid Fans<br>{int(total_avid_fans):,}</div>
<div class="scorecard casual">Total Casual Fans<br>{int(total_casual_fans):,}</div>
<div class="scorecard convertible">Total Convertible Fans<br>{int(total_convertible_fans):,}</div>
""", unsafe_allow_html=True)

# Create the map
folium_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Add markers to the map
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

# Render the map
folium_static(folium_map, width=1100, height=700)
