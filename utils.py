import pandas as pd
import folium
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_folium import folium_static

def apply_common_styles():
    st.markdown("""
    <style>
        /* Add common styles here */
    </style>
    """, unsafe_allow_html=True)

def load_and_filter_data(file_path: str, selected_income_levels=None):
    df = pd.read_parquet(file_path)
    if selected_income_levels:
        columns_to_show = ['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race'] + selected_income_levels
    else:
        columns_to_show = ['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race']
    
    filtered_df = df[columns_to_show]
    return filtered_df

def display_aggrid_table(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=False, groupable=True)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()
    AgGrid(df, gridOptions=gridOptions)

def add_map_markers(m, df, color_column, color_key):
    for idx, row in df.iterrows():
        try:
            lat = row['US lat']
            lon = row['US lon']
            color = color_key.get(row[color_column], 'blue')
            folium.Marker([lat, lon], icon=folium.Icon(color=color)).add_to(m)
        except KeyError as e:
            st.error(f"Column not found: {e}")
        except Exception as e:
            st.error(f"Error adding marker: {e}")
