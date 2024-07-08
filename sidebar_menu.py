import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from Pages import home_app, mlb_aapi_app, mlb_americanindian_app, mlb_asian_app, mlb_black_app, mlb_hispanic_app, mlb_white_app, chatbot_page_app

# Custom CSS for Sidebar Menu
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #1d1d1d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def sidebar_menu():
    # Load your dataframes here
    dataframes = {
        "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_AmericanIndian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
    }
    
    with st.sidebar:
        selected = option_menu(
            "Sports Analysis",
            ["Home", "MLB", "NBA", "NFL", "NHL", "MLS", "Chatbot"],
            icons=["house", "bar-chart-line", "bar-chart-line", "bar-chart-line", "bar-chart-line", "bar-chart-line", "robot"],
            menu_icon="cast",
            default_index=0,
        )

        if selected == "Home":
            return home_app.app
        elif selected == "MLB":
            submenu_items = {
                "AAPI": "MLB - AAPI",
                "American Indian": "MLB - American Indian",
                "Asian": "MLB - Asian",
                "Black": "MLB - Black",
                "Hispanic": "MLB - Hispanic",
                "White": "MLB - White"
            }
            submenu_selected = st.selectbox("Select Category", list(submenu_items.keys()))
            df = dataframes.get(submenu_items[submenu_selected])
            if submenu_selected == "AAPI":
                return lambda: mlb_aapi_app.app(df)
            elif submenu_selected == "American Indian":
                return lambda: mlb_americanindian_app.app(df)
            elif submenu_selected == "Asian":
                return lambda: mlb_asian_app.app(df)
            elif submenu_selected == "Black":
                return lambda: mlb_black_app.app(df)
            elif submenu_selected == "Hispanic":
                return lambda: mlb_hispanic_app.app(df)
            elif submenu_selected == "White":
                return lambda: mlb_white_app.app(df)
        elif selected == "NBA":
            st.write("NBA data will be available soon.")
        elif selected == "NFL":
            st.write("NFL data will be available soon.")
        elif selected == "NHL":
            st.write("NHL data will be available soon.")
        elif selected == "MLS":
            st.write("MLS data will be available soon.")
        elif selected == "Chatbot":
            return lambda: chatbot_page_app.app(dataframes)
        else:
            return None
