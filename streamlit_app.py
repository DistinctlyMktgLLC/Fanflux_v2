import streamlit as st

# Set page configuration at the very beginning
st.set_page_config(page_title="Fanflux", layout="wide")

# Importing the leagues analysis app function
from Pages.leagues_analysis import app as leagues_analysis_app

# Ensure the app function is called only once
def main():
    leagues_analysis_app()

if __name__ == "__main__":
    main()
