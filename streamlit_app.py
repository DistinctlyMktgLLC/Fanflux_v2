import streamlit as st
import pandas as pd
import sidebar_menu
import utils

# Function to apply common styles
def apply_common_styles():
    st.markdown(
        """
        <style>
        .reportview-container .markdown-text-container {
            font-family: Arial, sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #1d1d1d;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_common_styles()

# Initialize sidebar menu
dataframes = {
    "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
    "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_AmericanIndian.parquet"),
    "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
    "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
    "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
    "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
    # Add other dataframes if needed
}

page_function = sidebar_menu.sidebar_menu(dataframes)

if page_function:
    page_function()
else:
    st.error("Page not implemented yet.")
