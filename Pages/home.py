import streamlit as st

st.set_page_config(page_title="Fanflux Home", page_icon="🏆", layout="wide")

def app():
    st.markdown("# 🏆 Find Fans")
    st.markdown("Fanflux visualizes fan data from our database that shows where fans live, how much they make, and their team and league preferences. Just click on the widgets below to explore!")

if __name__ == "__main__":
    app()
