import streamlit as st
import pandas as pd
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

def load_dataframe(file_path):
    try:
        df = pd.read_parquet(file_path)
        required_columns = ["Race", "Team", "League", "Fandom Level", "Income Level"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.warning(f"File {file_path} is missing columns: {missing_columns}")
            return pd.DataFrame(columns=required_columns)
        return df
    except FileNotFoundError:
        st.warning(f"File not found: {file_path}")
        return pd.DataFrame(columns=required_columns)

def sidebar_menu():
    dataframes = {
        "MLB - AAPI": load_dataframe("data/Fanflux_Intensity_MLB_AAPI.parquet"),
        "MLB - American Indian": load_dataframe("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
        "MLB - Asian": load_dataframe("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": load_dataframe("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": load_dataframe("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": load_dataframe("data/Fanflux_Intensity_MLB_White.parquet"),
    }

    combined_df = pd.concat(dataframes.values(), ignore_index=True)

    menu_options = ["Home", "MLB - AAPI", "MLB - American Indian", "MLB - Asian", "MLB - Black", "MLB - Hispanic", "MLB - White", "Chatbot"]
    selected = st.sidebar.selectbox("Choose an option", menu_options)

    st.sidebar.header("Filter options")
    selected_race = st.sidebar.multiselect("Race", combined_df["Race"].unique())
    selected_team = st.sidebar.multiselect("Team", combined_df["Team"].unique())
    selected_league = st.sidebar.multiselect("League", combined_df["League"].unique())
    selected_fandom_level = st.sidebar.multiselect("Fandom Level", combined_df["Fandom Level"].unique())
    selected_income_level = st.sidebar.multiselect("Income Level", combined_df["Income Level"].unique())

    if selected_race:
        combined_df = combined_df[combined_df["Race"].isin(selected_race)]
    if selected_team:
        combined_df = combined_df[combined_df["Team"].isin(selected_team)]
    if selected_league:
        combined_df = combined_df[combined_df["League"].isin(selected_league)]
    if selected_fandom_level:
        combined_df = combined_df[combined_df["Fandom Level"].isin(selected_fandom_level)]
    if selected_income_level:
        combined_df = combined_df[combined_df["Income Level"].isin(selected_income_level)]

    if selected == "Home":
        return home_app.app
    elif selected == "MLB - AAPI":
        return mlb_aapi_app.app
    elif selected == "MLB - American Indian":
        return mlb_americanindian_app.app
    elif selected == "MLB - Asian":
        return mlb_asian_app.app
    elif selected == "MLB - Black":
        return mlb_black_app.app
    elif selected == "MLB - Hispanic":
        return mlb_hispanic_app.app
    elif selected == "MLB - White":
        return mlb_white_app.app
    elif selected == "Chatbot":
        st.write("Coming Soon")
        return chatbot_page_app.app
