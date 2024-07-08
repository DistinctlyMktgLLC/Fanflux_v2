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
        if any(word.capitalize() in df['Team'].unique() for df in dataframes.values()):
            filters['team'] = word.capitalize()
        elif word.lower() in ["avid", "casual", "moderate"]:
            filters['fandom_level'] = word.capitalize()
        elif word.lower() in ["mlb", "nba", "nfl", "nhl", "mls"]:
            filters['league'] = word.upper()
        elif word.lower() in ["affluent", "wealthy", "middle", "working", "struggling"]:
            filters['income_level'] = word.capitalize()
        elif word.lower() in ["white", "black", "asian", "hispanic", "aapi"]:
            filters['race'] = word.capitalize()
    
    return filters

def generate_bot_response(user_input, dataframes):
    filters = extract_filters(user_input, dataframes)
    st.write("Extracted Filters:", filters)
    
    filtered_data = pd.concat(dataframes.values())
    
    if filters['team']:
        filtered_data = filtered_data[filtered_data['Team'] == filters['team']]
    if filters['fandom_level']:
        filtered_data = filtered_data[filtered_data['Fandom Level'] == filters['fandom_level']]
    if filters['league']:
        filtered_data = filtered_data[filtered_data['League'] == filters['league']]
    if filters['income_level']:
        filtered_data = filtered_data[filtered_data['Income Level'] == filters['income_level']]
    if filters['race']:
        filtered_data = filtered_data[filtered_data['Race'] == filters['race']]
    
    st.write("Filtered Data:", filtered_data)
    
    response = f"Here are the results for your query: {filtered_data.to_dict(orient='records')}"
    return response

def app(dataframes):
    st.title("Chat with our Data Strategist")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask something about the data:")
    
    if user_input:
        response = generate_bot_response(user_input, dataframes)
        st.session_state.chat_history.append({"message": user_input, "is_user": True})
        st.session_state.chat_history.append({"message": response, "is_user": False})

    for chat in st.session_state.chat_history:
        st.write(chat["message"])

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
