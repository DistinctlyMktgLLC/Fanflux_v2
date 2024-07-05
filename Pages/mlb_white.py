# Pages/mlb_white.py
import streamlit as st
import utils
from streamlit_folium import st_folium
import leafmap.foliumap as leafmap

def app():
    st.title("White Baseball Fans Analysis")
    utils.apply_common_styles()

    df = utils.load_data("data/Fanflux_Intensity_MLB_White.parquet")

    if df.empty:
        st.error("No data available.")
        return

    # Rename 'Not at all' to 'Convertible' in the 'Fandom Level' column
    df['Fandom Level'] = df['Fandom Level'].replace('Not at all', 'Convertible')

    # Define the income columns
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

    # Calculate totals for each fan category by summing the income columns
    total_avid_fans = df[df['Fandom Level'] == 'Avid'][income_columns].sum().sum()
    total_casual_fans = df[df['Fandom Level'] == 'Casual'][income_columns].sum().sum()
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible'][income_columns].sum().sum()

    # Scorecards
    st.write("### Fan Demographics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Avid Fans", total_avid_fans)
    col2.metric("Total Casual Fans", total_casual_fans)
    col3.metric("Total Convertible Fans", total_convertible_fans)

    # Display the table
    st.write("### Filtered Data")
    st.dataframe(df, width=1200, height=400)

    # Create the map using leafmap
    st.write("### Fan Opportunity Map")

    m = leafmap.Map(center=[37.0902, -95.7129], zoom=4)
    for _, row in df.iterrows():
        total_fans = row[income_columns].sum()
        popup_content = (
            f"Team: {row['Team']}<br>"
            f"League: {row['League']}<br>"
            f"Neighborhood: {row['Neighborhood']}<br>"
            f"Fandom Level: {row['Fandom Level']}<br>"
            f"Race: {row['Race']}<br>"
            f"Total Fans: {total_fans}"
        )
        m.add_marker(location=[row['US lat'], row['US lon']], popup=popup_content)
    
    m.to_streamlit(height=700)
