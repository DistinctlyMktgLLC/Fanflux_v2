import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Fanflux", layout="wide")

from Pages.leagues_analysis import app as Leagues_analysis

# Run the leagues analysis page
Leagues_analysis()
