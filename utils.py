import streamlit as st
import folium
from streamlit_folium import st_folium

def apply_common_styles():
    st.markdown("""
        <style>
            .main-content {
                max-width: 90%;
                margin: 0 auto;
            }
            .scorecard {
                display: inline-block;
                width: 30%;
                border: 1px solid #ddd;
                padding: 10px;
                margin: 10px;
                text-align: center;
                background-color: #333;
                color: white;
            }
            .scorecard h3 {
                margin: 0;
                padding: 0;
                font-size: 24px;
            }
            .scorecard p {
                margin: 5px 0 0 0;
                padding: 0;
                font-size: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

def render_map(df):
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    
    # Define colors for different fandom levels
    color_dict = {
        'Avid': 'red',
        'Casual': 'green',
        'Convertible Fans': 'blue'
    }
    
    for _, row in df.iterrows():
        fandom_level = row['Fandom Level']
        marker_color = color_dict.get(fandom_level, 'gray')  # Default to gray if not found
        folium.Marker(
            location=[row['US lat'], row['US lon']],
            popup=folium.Popup(
                f"Neighborhood: {row['Neighborhood']}<br>"
                f"Race: {row['Race']}<br>"
                f"Team: {row['Team']}<br>"
                f"League: {row['League']}<br>"
                f"Fandom Level: {row['Fandom Level']}<br>"
                f"Total Fans: {row[['Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
                                 'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
                                 'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
                                 'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
                                 'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
                                 'Affluent ($200,000 or more)']].sum()}"
            ),
            icon=folium.Icon(color=marker_color, icon='info-sign')
        ).add_to(m)
    
    st_folium(m, width=700, height=500)
