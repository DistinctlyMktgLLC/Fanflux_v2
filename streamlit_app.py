# streamlit_app.py
import streamlit as st
import sidebar_menu

page_function = sidebar_menu.sidebar_menu()
page_function()
