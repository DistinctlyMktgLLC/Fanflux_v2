import streamlit as st

# Set page configuration
st.set_page_config(page_title="Fanflux", layout="wide")

# Importing the leagues analysis app function
from Pages.leagues_analysis import app as Leagues_analysis

# Run the app function
Leagues_analysis()
