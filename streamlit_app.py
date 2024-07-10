# streamlit_app.py
import streamlit as st
import sidebar_menu

# Apply common styles
from utils import apply_common_styles
apply_common_styles()

# Call the sidebar menu and get the selected page function
page_function = sidebar_menu.sidebar_menu()

# Run the selected page function
page_function()
