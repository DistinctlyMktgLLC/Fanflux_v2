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
    st.write("Extracted Filters:", filters)
    
    combined_data = pd.concat(dataframes.values())
    filtered_data = combined_data.copy()
    
    if filters['team']:
        filtered_data = filtered_data[filtered_data['Team'] == filters['team']]
    # Add similar filtering logic for other filters
    
    response_detail = filtered_data.to_dict(orient='records')
    response = (
        f"Here's a fascinating insight for you: {response_detail}. "
        "Isn't it intriguing how data can reveal such stories? Let's dive deeper!"
    )
    
    return response

def app(dataframes):
    st.title("Chat with our Data Strategist")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        st.write(f"**{chat['message']}**")
        st.write(chat['response'])
        
    user_input = st.text_input("Ask something about the data:")

    if user_input:
        response = generate_bot_response(user_input, dataframes)
        st.session_state.chat_history.append({"message": user_input, "response": response})

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
