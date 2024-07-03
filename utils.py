import streamlit as st
import pandas as pd
from utils import load_data, create_map, add_map_markers, apply_common_styles
from streamlit_folium import st_folium

def app():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    
    st.title("White Baseball Fans")

    df = load_data("data/Fanflux_Intensity_MLB_White.parquet")  # Adjust the file path accordingly

    if df.empty:
        st.error("No data available.")
        return

    # Display the available columns for debugging
    st.write("DataFrame Columns:")
    st.write(df.columns.tolist())

    st.sidebar.header("Filter Options")
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    fandom_level = st.sidebar.selectbox('Select Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))

    income_levels = [
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

    selected_income_levels = st.sidebar.multiselect('Select Income Levels', income_levels, default=income_levels)

    # Filter the DataFrame based on selections
    filtered_df = df[
        (df['Team'] == team) &
        (df['Fandom Level'] == fandom_level)
    ]

    if not filtered_df.empty:
        filtered_df['Total Fans'] = filtered_df[selected_income_levels].sum(axis=1)
        st.write("Filtered Data")
        st.write(filtered_df)

        m = create_map()
        color_key = {
            "Avid": "green",
            "Casual": "orange",
            "Convertible": "blue"
        }
        add_map_markers(m, filtered_df, 'Fandom Level', color_key)
        st_folium(m, width=700, height=500)
    else:
        st.warning("No matching data found.")

    # Display the Streamlit table
    st.dataframe(filtered_df, height=400)

# Ensure that the utils.py file contains the correct imports and functions
