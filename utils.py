import streamlit as st
import folium
from streamlit_folium import folium_static

def apply_common_styles():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #2E2E2E;
            color: white;
        }
        .sidebar .sidebar-content a {
            color: white;
            text-decoration: none;
        }
        .sidebar .sidebar-content a:hover {
            color: #F39C12;
        }
        .sidebar .sidebar-content .stRadio label {
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_map(df):
    # Define colors for different Fandom Levels
    fandom_colors = {
        'Avid': 'red',
        'Casual': 'blue',
        'Convertible Fans': 'green'
    }

    # Create a Folium map
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=5)

    for _, row in df.iterrows():
        # Get the color for the Fandom Level
        color = fandom_colors.get(row['Fandom Level'], 'gray')

        # Total Fans calculation
        total_fans = row[['Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
                          'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
                          'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
                          'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
                          'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
                          'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
                          'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
                          'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)']].sum()

        # Marker popup content
        popup_content = (
            f"Neighborhood: {row['Neighborhood']}<br>"
            f"Race: {row['Race']}<br>"
            f"Team: {row['Team']}<br>"
            f"League: {row['League']}<br>"
            f"Fandom Level: {row['Fandom Level']}<br>"
            f"Total Fans: {total_fans}"
        )

        folium.Marker(
            location=[row['US lat'], row['US lon']],
            popup=popup_content,
            icon=folium.Icon(color=color)
        ).add_to(m)

    # Display the map in Streamlit
    folium_static(m)
