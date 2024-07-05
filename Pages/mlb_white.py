# Pages/mlb_white.py
import streamlit as st
import utils
from streamlit_folium import st_folium

def app():
    st.title("White Baseball Fans Analysis")
    utils.apply_common_styles()

    df = utils.load_data("data/Fanflux_Intensity_MLB_White.parquet")

    if df.empty:
        st.error("No data available.")
        return

    # Calculate totals for each fan category
    total_avid_fans = df[df['Fandom Level'] == 'Avid']['Total Fans'].sum()
    total_casual_fans = df[df['Fandom Level'] == 'Casual']['Total Fans'].sum()
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible']['Total Fans'].sum()

    # Scorecards
    st.write("### Fan Demographics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Avid Fans", total_avid_fans)
    col2.metric("Total Casual Fans", total_casual_fans)
    col3.metric("Total Convertible Fans", total_convertible_fans)

    # Display the table
    st.write("### Filtered Data")
    st.dataframe(df, width=1200, height=400)

    # Create the map
    st.write("### Fan Opportunity Map")
    color_key = {
        'Avid': 'red',
        'Casual': 'blue',
        'Convertible': 'green'
    }
    m = utils.create_map(df, 'Fandom Level', color_key)
    st_folium(m, width=700, height=500)
