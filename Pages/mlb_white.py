# mlb_white.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

def app():
    st.title("White Baseball Fans Analysis")

    # Load data
    df = pd.read_csv('data/Fanflux_Intensity_MLB_White.csv')

    # Custom CSS for scorecards and general styling
    st.markdown(
        """
        <style>
        body {
            font-family: 'Roboto Mono', monospace;
        }

        .metric-container {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }

        .metric-card {
            background-color: black;
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            flex: 1;
            margin: 0 10px;
            position: relative;
        }

        .metric-card:before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 5px;
            border-radius: 10px 0 0 10px;
        }

        .metric-card.avid:before {
            background-color: red;
        }

        .metric-card.casual:before {
            background-color: blue;
        }

        .metric-card.convertible:before {
            background-color: green;
        }

        .leaflet-container {
            width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Calculate totals for each fan category
    total_avid_fans = df[df['Fandom Level'] == 'Avid'][[
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
        'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
        'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
        'Affluent ($200,000 or more)']].sum().sum()

    total_casual_fans = df[df['Fandom Level'] == 'Casual'][[
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
        'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
        'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
        'Affluent ($200,000 or more)']].sum().sum()

    total_convertible_fans = df[df['Fandom Level'] == 'Convertible'][[
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
        'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
        'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
        'Affluent ($200,000 or more)']].sum().sum()

    # Scorecards
    st.write("### Fan Demographics")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metric-card avid'><h3>Total Avid Fans</h3><p>{total_avid_fans}</p></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card casual'><h3>Total Casual Fans</h3><p>{total_casual_fans}</p></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-card convertible'><h3>Total Convertible Fans</h3><p>{total_convertible_fans}</p></div>", unsafe_allow_html=True)

    # Map
    st.write("### Fan Opportunity Map")
    folium_map = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    # Colors for Fandom Level
    colors = {
        'Avid': 'red',
        'Casual': 'blue',
        'Convertible': 'green'
    }

    for idx, row in df.iterrows():
        total_fans = row[['Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
                          'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
                          'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
                          'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
                          'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
                          'Affluent ($200,000 or more)']].sum()
        popup_content = (
            f"Team: {row['Team']}<br>"
            f"League: {row['League']}<br>"
            f"Neighborhood: {row['Neighborhood']}<br>"
            f"Fandom Level: {row['Fandom Level']}<br>"
            f"Race: {row['Race']}<br>"
            f"Total Fans: {total_fans}"
        )
        color = colors.get(row['Fandom Level'], '#000000')
        folium.CircleMarker(
            location=[row['US lat'], row['US lon']],
            radius=5,
            popup=popup_content,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(folium_map)

    st_folium(folium_map, width=1200, height=600)

if __name__ == "__main__":
    app()
