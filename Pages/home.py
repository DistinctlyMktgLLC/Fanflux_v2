import streamlit as st
import utils

def app():
    utils.apply_common_styles()

    st.markdown(
        """
        <div class="hero-section">
            <h1>Welcome to Fanflux</h1>
            <p>Where Data Tells the Story of MLB Fandom</p>
            <a href="#features" class="cta-button">Get Started</a>
        </div>

        <div id="features" class="features-section">
            <div class="feature">
                <h3>Detailed Demographics</h3>
                <p>Uncover the age, race, and socio-economic status of fans from every team, league, and neighborhood.</p>
            </div>
            <div class="feature">
                <h3>Fandom Levels</h3>
                <p>Understand the intensity of fandom, from die-hard fans to casual viewers.</p>
            </div>
            <div class="feature">
                <h3>Interactive Visualizations</h3>
                <p>Dive into interactive maps and dynamic charts that bring the data to life.</p>
            </div>
        </div>

        <div class="footer">
            <p>&copy; 2024 Fanflux. All rights reserved.</p>
            <p>In partnership with <strong>DonnLynn Partners</strong></p>
            <p>Contact us: <a href="mailto:info@fanflux.com">info@fanflux.com</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    app()
