import streamlit as st
import pandas as pd

def extract_filters(user_input):
    filters = {
        "race": None,
        "fandom_level": None,
        "team": None,
        "league": None,
        "income_level": None
    }

    words = user_input.split()
    for word in words:
        if word.capitalize() in dataframes['MLB - AAPI']['Team'].unique():
            filters['team'] = word.capitalize()
        if word.capitalize() in dataframes['MLB - AAPI']['Fandom Level'].unique():
            filters['fandom_level'] = word.capitalize()
        if word.capitalize() in dataframes['MLB - AAPI']['League'].unique():
            filters['league'] = word.capitalize()
        if word in dataframes['MLB - AAPI'].columns[14:]:
            filters['income_level'] = word

    return filters

def generate_bot_response(user_input, dataframes):
    user_input = user_input.lower()
    combined_data = pd.concat(dataframes.values())

    filters = extract_filters(user_input)

    filtered_data = combined_data
    if filters['race']:
        filtered_data = filtered_data[filtered_data['Race'] == filters['race']]
    if filters['fandom_level']:
        filtered_data = filtered_data[filtered_data['Fandom Level'] == filters['fandom_level']]
    if filters['team']:
        filtered_data = filtered_data[filtered_data['Team'] == filters['team']]
    if filters['league']:
        filtered_data = filtered_data[filtered_data['League'] == filters['league']]
    if filters['income_level']:
        filtered_data['Total Convertible Fans'] = filtered_data[filters['income_level']].sum(axis=1)

    response_detail = f"for {' and '.join([f'{k}: {v}' for k, v in filters.items() if v])}: \n"
    response_detail += str(filtered_data.to_dict(orient='records'))

    response = (
        f"Here's a fascinating insight for you: {response_detail}. "
        f"Isn't it intriguing how data can reveal such stories? Let's dig deeper if you have more questions!"
    )

    return response

def app(dataframes):
    st.title("Chat with our Data Strategist")

    user_input = st.text_input("Ask something about the data:")

    if user_input:
        response = generate_bot_response(user_input, dataframes)
        st.write(response)

    st.write("Extracted Filters:", extract_filters(user_input))
    st.write("Filtered Data:", filtered_data)
