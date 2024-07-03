import streamlit as st
import pandas as pd
import utils
from streamlit_folium import st_folium

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

def app():
    utils.apply_common_styles()
    
    st.sidebar.title("Filters")
    
    df = utils.load_data('data/Fanflux_Intensity_MLB_White.parquet')
    
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    income_level = st.sidebar.selectbox('Select Income Levels', ['Choose an option'] + sorted(df.columns[df.columns.str.contains('[$]')].tolist()))

    if team != 'Choose an option':
        df = df[df['Team'] == team]
    
    if income_level != 'Choose an option':
        df = df[df[income_level] > 0]
    
    # Show selected columns
    selected_columns = ['Team', 'League', 'Neighborhood', 'Fandom Level', 'Race', 'zipcode']
    selected_columns += df.columns[df.columns.str.contains('[$]')].tolist()

    filtered_df = df[selected_columns]
    
    # Adjust zip code format
    filtered_df['zipcode'] = filtered_df['zipcode'].astype(str).str.zfill(5)

    # Display Datatable
    st.write("## Fan Opportunity Table")
    utils.create_table(filtered_df)
    
    # Create map
    st.write("## Fan Opportunity Map")
    m = utils.create_map()
    color_key = {'Avid': 'red', 'Casual': 'green', 'Convertible': 'blue'}
    utils.add_map_markers(m, filtered_df, 'Fandom Level', color_key)
    st_folium(m, width=700, height=500)

if __name__ == "__main__":
    app()
