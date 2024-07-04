import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# Set page configuration
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Hide export buttons
hide_export_buttons = """
    <style>
    .stActionButton {display: none;}
    .ag-header-row .ag-header-cell-menu-button {display: none;}
    </style>
"""
st.markdown(hide_export_buttons, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_parquet('data/Fanflux_Intensity_MLB_White.parquet')
    return df

df = load_data()

# Function to create styled scorecards
def create_scorecard(title, value, color):
    return f"""
    <div style="background-color: #000; padding: 20px; border-radius: 10px; width: 30%; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
        <div style="background-color: {color}; height: 100%; width: 10px; float: left; border-radius: 10px 0 0 10px;"></div>
        <h2 style="color: white; margin-left: 15px;">{title}</h2>
        <p style="color: white; font-size: 24px; margin-left: 15px;">{value}</p>
    </div>
    """

# Calculate totals for scorecards
total_avid = df[df['Fandom Level'] == 'Avid']['Fandom Level'].count()
total_casual = df[df['Fandom Level'] == 'Casual']['Fandom Level'].count()
total_convertible = df[df['Fandom Level'] == 'Convertible Fans']['Fandom Level'].count()

# Display scorecards
st.markdown(f"""
<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
    {create_scorecard('Avid Fans', total_avid, '#ff6347')}
    {create_scorecard('Casual Fans', total_casual, '#ffa500')}
    {create_scorecard('Convertible Fans', total_convertible, '#1e90ff')}
</div>
""", unsafe_allow_html=True)

# Display the map
st.title("Marker Cluster")
m = leafmap.Map(center=[40, -100], zoom=4)
cities = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"

m.add_geojson(regions, layer_name="US Regions")
m.add_points_from_xy(
    cities,
    x="longitude",
    y="latitude",
    color_column="region",
    icon_names=["gear", "map", "leaf", "globe"],
    spin=True,
    add_legend=True,
)

m.to_streamlit(height=700)
