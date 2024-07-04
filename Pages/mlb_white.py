import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium
from folium.plugins import MarkerCluster

def display_scorecards(df, income_levels):
    st.markdown(
        """
        <style>
        .scorecard-avid {
            background-color: #000000;
            color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.5);
            margin: 10px;
            text-align: center;
            position: relative;
        }
        .scorecard-avid::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 10px;
            height: 100%;
            background-color: #e74c3c;
            border-radius: 10px 0 0 10px;
        }

        .scorecard-casual {
            background-color: #000000;
            color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.5);
            margin: 10px;
            text-align: center;
            position: relative;
        }
        .scorecard-casual::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 10px;
            height: 100%;
            background-color: #f39c12;
            border-radius: 10px 0 0 10px;
        }

        .scorecard-convertible {
            background-color: #000000;
            color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.5);
            margin: 10px;
            text-align: center;
            position: relative;
        }
        .scorecard-convertible::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 10px;
            height: 100%;
            background-color: #3498db;
            border-radius: 10px 0 0 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Calculate the sum of income columns for each fandom level
    income_sum_avid = df[df['Fandom Level'] == 'Avid'][income_levels].sum().sum()
    income_sum_casual = df[df['Fandom Level'] == 'Casual'][income_levels].sum().sum()
    income_sum_convertible = df[df['Fandom Level'] == 'Convertible Fans'][income_levels].sum().sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="scorecard-avid"><h3>Avid Fans</h3><div class="value">{income_sum_avid}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="scorecard-casual"><h3>Casual Fans</h3><div class="value">{income_sum_casual}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="scorecard-convertible"><h3>Convertible Fans</h3><div class="value">{income_sum_convertible}</div></div>', unsafe_allow_html=True)

def display_table(df):
    st.dataframe(df)

def interactive_map(df):
    col1, col2 = st.columns([4, 1])
    options = list(leafmap.basemaps.keys())
    index = options.index("OpenTopoMap")

    with col2:
        basemap = st.selectbox("Select a basemap:", options, index)
    with col1:
        m = leafmap.Map(
            locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
        )
        m.add_basemap(basemap)
        
        # Clustering with correct column names and tooltips
        if 'US lat' in df.columns and 'US lon' in df.columns:
            marker_cluster = MarkerCluster().add_to(m)
            for _, row in df.iterrows():
                lat = row['US lat']
                lon = row['US lon']
                fandom_level = row['Fandom Level']
                if fandom_level == 'Avid':
                    color = 'red'
                elif fandom_level == 'Casual':
                    color = 'orange'
                else:
                    color = 'blue'
                
                income_levels = '<br>'.join(
                    [f'{col}: {row[col]}' for col in row.index 
                     if col.startswith(('Struggling', 'Getting', 'Starting', 'Middle', 'Comfortable', 'Doing', 'Prosperous', 'Wealthy', 'Affluent')) 
                     and row[col] > 0]
                )
                
                tooltip_text = (
                    f"Team: {row['Team']}<br>"
                    f"League: {row['League']}<br>"
                    f"City: {row['City']}<br>"
                    f"Fandom
