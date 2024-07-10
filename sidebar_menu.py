# sidebar_menu.py
import streamlit as st
from Pages import home, chatbot_page, league_page
from utils import apply_common_styles

def sidebar_menu():
    menu_options = {
        "🏠 Home": home.app,
        "📣 Leagues": league_page.app,
        "🤖 Chatbot": chatbot_page.app,
    }

    with st.sidebar:
        selected = st.selectbox("Fanflux", options=list(menu_options.keys()), format_func=lambda x: x.split(":")[1].strip() if ":" in x else x)

    apply_common_styles()
    menu_options[selected]()
