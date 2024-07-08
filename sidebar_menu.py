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

# Dictionary of dataframes
dataframes = {
    "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
    "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_AmericanIndian.parquet"),
    "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
    "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
    "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
    "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
}

def preprocess_dataframe(df):
    df['Fandom Level'] = df['Fandom Level'].replace("Not at All", "Convertible")
    return df

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Sports Analysis",
            options=["Home", "MLB", "NBA", "NFL", "NHL", "MLS", "Chatbot"],
            icons=["house", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "chat"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#1d1d1d"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#343a40"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )

        submenu_items = {
            "MLB": {
                "AAPI": mlb_aapi_app,
                "American Indian": mlb_americanindian_app,
                "Asian": mlb_asian_app,
                "Black": mlb_black_app,
                "Hispanic": mlb_hispanic_app,
                "White": mlb_white_app,
            },
            "NBA": {},
            "NFL": {},
            "NHL": {},
            "MLS": {}
        }

        if selected == "Home":
            return home_app
        elif selected == "Chatbot":
            return lambda: chatbot_page_app(dataframes)
        elif selected in submenu_items:
            if submenu_items[selected]:
                submenu_selected = st.selectbox("Select Category", list(submenu_items[selected].keys()))
                df = preprocess_dataframe(dataframes.get(f"MLB - {submenu_selected}", pd.DataFrame()))

                if not df.empty:
                    team_options = df['Team'].unique().tolist()
                    fandom_level_options = df['Fandom Level'].unique().tolist()
                    league_options = df['League'].unique().tolist()
                    income_level_options = df.columns[14:].tolist()

                    selected_team = st.multiselect("Select Team(s)", team_options)
                    selected_fandom_level = st.multiselect("Select Fandom Level(s)", fandom_level_options)
                    selected_league = st.multiselect("Select League(s)", league_options)
                    selected_income_level = st.multiselect("Select Income Level(s)", income_level_options)

                    filtered_df = df.copy()
                    if selected_team:
                        filtered_df = filtered_df[filtered_df['Team'].isin(selected_team)]
                    if selected_fandom_level:
                        filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom_level)]
                    if selected_league:
                        filtered_df = filtered_df[filtered_df['League'].isin(selected_league)]

                    if selected_income_level:
                        filtered_df['Total Convertible Fans'] = filtered_df[selected_income_level].sum(axis=1)
                    else:
                        filtered_df['Total Convertible Fans'] = 0

                    return lambda: submenu_items[selected][submenu_selected](filtered_df)
                else:
                    st.error("No data available for the selected category.")
                    return None
            else:
                st.error("No subpages available for the selected league.")
                return None
        else:
            return lambda: st.error("Page not implemented yet.")
