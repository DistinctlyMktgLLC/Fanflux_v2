import streamlit as st
from Pages.leagues_analysis import app as Leagues_analysis

st.set_page_config(page_title="Fanflux", layout="wide")

Leagues_analysis()
