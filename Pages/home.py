import streamlit as st
import utils

def app():
    utils.apply_common_styles()
    st.markdown(
        """
        # Welcome to Fanflux

        Where Data Tells the Story of Fandom

        ## Detailed Demographics
        Uncover the age, race, and socio-economic status of fans from every team, league, and neighborhood.

        ## Fandom Levels
        Understand the intensity of fandom, from die-hard fans to casual viewers.

        ## Interactive Visualizations
        Dive into interactive maps and dynamic charts that bring the data to life.
        """
    )
