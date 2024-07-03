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

        <div style="position: fixed; bottom: 0; width: 100%; background-color: #333; color: white; text-align: center; padding: 10px 0;">
            © 2024 Fanflux. All rights reserved.
            <br>In partnership with DonnLynn Partners
            <br>Contact us: <a href="mailto:info@distinctlymktg.com" style="color: #F39C12;">info@distinctlymktg.com</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
