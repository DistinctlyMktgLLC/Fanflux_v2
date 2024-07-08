import streamlit as st
import sidebar_menu
import utils

# Initialize CSS styles
utils.apply_common_styles()

# Initialize sidebar menu
page_function = sidebar_menu.sidebar_menu()

if page_function:
    page_function()
else:
    st.write("Welcome to the Fanflux dashboard!")
