import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

def app():
    st.title("White Baseball Fans Analysis")

    # Load your data
    df = pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")

    # Colors for each fandom level
    colors = {
        "Avid": "red",
        "Casual": "blue",
        "Convertible": "green",
        "Not at all": "black"  # Just in case there are still rows with this value
    }

    # Replace "Not at all" with "Convertible"
    df['Fandom Level'] = df['Fandom Level'].replace("Not at all", "Convertible")

    # Define income columns
    income_columns = [
        "Struggling (Less than $10,000)",
        "Getting By ($10,000 to $14,999)",
        "Getting By ($15,000 to $19,999)",
        "Starting Out ($20,000 to $24,999)",
        "Starting Out ($25,000 to $29,999)",
        "Starting Out ($30,000 to $34,999)",
        "Middle Class ($35,000 to $39,999)",
        "Middle Class ($40,000 to $44,999)",
        "Middle Class ($45,000 to $49,999)",
        "Comfortable ($50,000 to $59,999)",
        "Comfortable ($60,000 to $74,999)",
        "Doing Well ($75,000 to $99,999)",
        "Prosperous ($100,000 to $124,999)",
        "Prosperous ($125,000 to $149,999)",
        "Wealthy ($150,000 to $199,999)",
        "Affluent ($200,000 or more)"
    ]

    # Calculate totals for each fan category
    total_avid_fans = df[df['Fandom Level'] == 'Avid'][income_columns].sum().sum()
    total_casual_fans = df[df['Fandom Level'] == 'Casual'][income_columns].sum().sum()
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible'][income_columns].sum().sum()

    # Custom CSS for scorecards
    scorecard_style = """
    <style>
    .scorecard {
        background-color: black;
        color: white;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .scorecard .highlight {
        width: 5px;
        height: 100%;
        margin-right: 10px;
    }
    .scorecard .value {
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(scorecard_style, unsafe_allow_html=True)

    # Display scorecards
    st.write("### Fan Demographics")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="scorecard"><div class="highlight" style="background-color: red;"></div><div class="value">Total Avid Fans<br>{total_avid_fans}</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="scorecard"><div class="highlight" style="background-color: blue;"></div><div class="value">Total Casual Fans<br>{total_casual_fans}</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="scorecard"><div class="highlight" style="background-color: green;"></div><div class="value">Total Convertible Fans<br>{total_convertible_fans}</div></div>', unsafe_allow_html=True)

    # Map rendering
    st.write("### Fan Opportunity Map")
    folium_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    for index, row in df.iterrows():
        try:
            # Create popup content
            popup_content = (
                f"Team: {row['Team']}<br>"
                f"League: {row['League']}<br>"
                f"Neighborhood: {row['Neighborhood']}<br>"
                f"Fandom Level: {row['Fandom Level']}<br>"
                f"Race: {row['Race']}<br>"
                f"Total Fans: {row[income_columns].sum()}"
            )

            # Determine the color based on the Fandom Level
            color = colors.get(row['Fandom Level'], 'black')

            # Check for valid coordinates
            lat = row['US lat']
            lon = row['US lon']
            if pd.notna(lat) and pd.notna(lon):
                # Add the CircleMarker to the map
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=5,
                    popup=popup_content,
                    color=color,
                    fill=True,
                    fill_color=color
                ).add_to(folium_map)
            else:
                print(f"Invalid coordinates for row {index}: lat={lat}, lon={lon}")

        except KeyError as e:
            print(f"KeyError for row {index}: {e}")
        except Exception as e:
            print(f"Unexpected error for row {index}: {e}")

    # Display the map in Streamlit
    folium_static(folium_map, width=1100)
