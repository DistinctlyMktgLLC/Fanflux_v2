import streamlit as st
import pandas as pd
from Pages import home, mlb_aapi, mlb_americanindian, mlb_asian, mlb_black, mlb_hispanic, mlb_white, chatbot_page

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
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
        # Add other leagues' dataframes here
    }

    # Combine all dataframes into one for filtering
    combined_df = pd.concat(dataframes.values())

    menu_options = ["Home", "MLB - AAPI", "MLB - American Indian", "MLB - Asian", "MLB - Black", "MLB - Hispanic", "MLB - White", "Chatbot"]
    selected = st.sidebar.selectbox("Choose an option", menu_options)

    # Filters
    st.sidebar.header("Filter options")
    selected_race = st.sidebar.multiselect("Race", combined_df["Race"].unique())
    selected_team = st.sidebar.multiselect("Team", combined_df["Team"].unique())
    selected_league = st.sidebar.multiselect("League", combined_df["League"].unique())
    selected_fandom_level = st.sidebar.multiselect("Fandom Level", combined_df["Fandom_Level"].unique())
    selected_income_level = st.sidebar.multiselect("Income Level", combined_df["Income_Level"].unique())

    # Apply filters
    if selected_race:
        combined_df = combined_df[combined_df["Race"].isin(selected_race)]
    if selected_team:
        combined_df = combined_df[combined_df["Team"].isin(selected_team)]
    if selected_league:
        combined_df = combined_df[combined_df["League"].isin(selected_league)]
    if selected_fandom_level:
        combined_df = combined_df[combined_df["Fandom_Level"].isin(selected_fandom_level)]
    if selected_income_level:
        combined_df = combined_df[combined_df["Income_Level"].isin(selected_income_level)]

    # Display filtered results (for debugging purposes only, should be removed later)
    st.dataframe(combined_df)

    # Return the app corresponding to the selected menu option
    if selected == "Home":
        return home.app
    elif selected == "MLB - AAPI":
        return mlb_aapi.app
    elif selected == "MLB - American Indian":
        return mlb_americanindian.app
    elif selected == "MLB - Asian":
        return mlb_asian.app
    elif selected == "MLB - Black":
        return mlb_black.app
    elif selected == "MLB - Hispanic":
        return mlb_hispanic.app
    elif selected == "MLB - White":
        return mlb_white.app
    elif selected == "Chatbot":
        return chatbot_page.app
