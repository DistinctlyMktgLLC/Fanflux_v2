import streamlit as st
import sidebar_menu

# Set up the page title
st.set_page_config(page_title="Fanflux Dashboard")

# Call the sidebar menu function
page_function = sidebar_menu.sidebar_menu()

# Run the selected page function
if page_function:
    page_function()
