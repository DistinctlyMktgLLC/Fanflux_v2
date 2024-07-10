# sidebar_menu.py
import streamlit as st
from Pages import home_app, chatbot_page_app, leagues_app
from utils import apply_common_styles

def sidebar_menu():
    menu_options = {
        "🏠 Home": home_app,
        "📣 Leagues": leagues_app,
        "🤖 Chatbot": chatbot_page_app,
    }

    with st.sidebar:
        selected = st.selectbox("Fanflux", options=list(menu_options.keys()), format_func=lambda x: x.split(":")[1].strip() if ":" in x else x)

    apply_common_styles()
    menu_options[selected]()
