# sidebar_menu.py
import streamlit as st
from streamlit_option_menu import option_menu
from Pages import home, mlb_page, chatbot_page

# Load the foam finger image
foam_finger_path = "data/istockphoto-1305157472-612x612.jpg"

menu_options = {
    "🏠 Home": home.app,
    "Leagues": {
        "MLB": mlb_page.app,
        "NBA": nba_page.app,  # Add NBA, NFL, NHL, Soccer pages similarly
        "NFL": nfl_page.app,
        "NHL": nhl_page.app,
        "MLS": mls_page.app,
    },
    "🤖 Chatbot": chatbot_page.app
}

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Fanflux",
            options=list(menu_options.keys()),
            icons=["house", foam_finger_path, "robot"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical"
        )

        if selected == "Leagues":
            sub_selected = option_menu(
                menu_title="Leagues",
                options=list(menu_options["Leagues"].keys()),
                icons=["baseball", "basketball", "football", "hockey", "soccer"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical"
            )
            page_function = menu_options["Leagues"][sub_selected]
        else:
            page_function = menu_options[selected]

    page_function()
