# multiapp.py

import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        st.sidebar.title('Navigation')
        app = st.sidebar.selectbox(
            'Go to',
            self.apps,
            format_func=lambda app: app['title']
        )

        app['function']()
