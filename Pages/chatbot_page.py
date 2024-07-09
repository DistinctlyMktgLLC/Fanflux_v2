import streamlit as st
import pandas as pd

def extract_filters(user_input, dataframes):
    filters = {
        "race": None,
        "fandom_level": None,
        "team": None,
        "league": None,
        "income_level": None,
    }

    words = user_input.split()
    for word in words:
        if word.capitalize() in dataframes['MLB - AAPI']['Team'].unique():
            filters['team'] = word.capitalize()
            break
    # Add similar logic for other filters
    return filters

def generate_bot_response(user_input, dataframes):
    filters = extract_filters(user_input, dataframes)
    filtered_data = pd.DataFrame()
    
    for df in dataframes.values():
        if filters['team']:
            df = df[df['Team'] == filters['team']]
        # Apply other filters similarly
        filtered_data = pd.concat([filtered_data, df])
    
    st.write("Extracted Filters:")
    st.json(filters)
    st.write("Filtered Data:", filtered_data.head())  # For debugging

def app(dataframes):
    st.title("Chat with our Data Strategist")
    user_input = st.text_input("Ask something about the data:")
    
    if user_input:
        generate_bot_response(user_input, dataframes)

    if st.button("Clear Chat"):
        st.experimental_rerun()
