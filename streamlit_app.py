# streamlit_app.py
import streamlit as st
from multiapp import MultiApp
import Pages.home as home
import Pages.mlb_white as white

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

app = MultiApp()

app.add_app("Home", home.app)
app.add_app("White Baseball Fans", white.app)

app.run()
