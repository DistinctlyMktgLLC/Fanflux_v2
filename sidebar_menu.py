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

def sidebar_menu(dataframes):
    # Define the options
    options = ["Home", "MLB", "NBA", "NFL", "NHL", "MLS", "Chatbot"]
    submenu_items = {
        "MLB": ["AAPI", "American Indian", "Asian", "Black", "Hispanic", "White"],
        # Add other submenus if needed
    }

    selected = option_menu(
        menu_title="Sports Analysis",
        options=options,
        icons=["house", "bar-chart-line", "bar-chart-line", "bar-chart-line", "bar-chart-line", "bar-chart-line", "chat-dots"],
        menu_icon="cast",
        default_index=0,
    )

    if selected == "Home":
        return home_app
    elif selected == "Chatbot":
        return lambda: chatbot_page_app(dataframes)
    elif selected in submenu_items:
        if submenu_items[selected]:
            submenu_selected = st.selectbox("Select Category", list(submenu_items[selected]))
            df = preprocess_dataframe(dataframes.get(f"MLB - {submenu_selected}", pd.DataFrame()))
            return lambda: show_data_page(df)
    return None

def preprocess_dataframe(df):
    # Implement your dataframe preprocessing here if needed
    return df

def show_data_page(df):
    st.dataframe(df)
