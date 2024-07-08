# Pages/chatbot.py
import streamlit as st
from streamlit_chat import message
import re
import pandas as pd

def extract_filters(user_input, combined_data):
    filters = {
        'race': None,
        'fandom_level': None,
        'team': None,
        'league': None,
        'income_level': None
    }

    # Define possible values for each filter
    races = ["AAPI", "American Indian", "Asian", "Black", "Hispanic", "White"]
    fandom_levels = ["Avid", "Casual", "Convertible"]
    leagues = ["MLB", "NBA", "NFL", "NHL", "MLS"]

    # Extract race
    for race in races:
        if race.lower() in user_input:
            filters['race'] = race
            break

    # Extract fandom level
    for level in fandom_levels:
        if level.lower() in user_input:
            filters['fandom_level'] = level
            break

    # Extract league
    for league in leagues:
        if league.lower() in user_input:
            filters['league'] = league
            break

    # Extract team
    for team in combined_data['Team'].unique():
        if team.lower() in user_input:
            filters['team'] = team
            break

    # Extract income levels using regex to match ranges
    income_pattern = re.compile(r"\$?(\d{1,3}(?:,\d{3})*)(?:\sto\s\$?(\d{1,3}(?:,\d{3})*))?")
    match = income_pattern.search(user_input)
    if match:
        min_income = int(match.group(1).replace(',', ''))
        max_income = int(match.group(2).replace(',', '')) if match.group(2) else None

        income_levels = [
            ('Struggling (Less than $10,000)', 0, 9999),
            ('Getting By ($10,000 to $14,999)', 10000, 14999),
            ('Getting By ($15,000 to $19,999)', 15000, 19999),
            ('Starting Out ($20,000 to $24,999)', 20000, 24999),
            ('Starting Out ($25,000 to $29,999)', 25000, 29999),
            ('Starting Out ($30,000 to $34,999)', 30000, 34999),
            ('Middle Class ($35,000 to $39,999)', 35000, 39999),
            ('Middle Class ($40,000 to $44,999)', 40000, 44999),
            ('Middle Class ($45,000 to $49,999)', 45000, 49999),
            ('Comfortable ($50,000 to $59,999)', 50000, 59999),
            ('Comfortable ($60,000 to $74,999)', 60000, 74999),
            ('Doing Well ($75,000 to $99,999)', 75000, 99999),
            ('Prosperous ($100,000 to $124,999)', 100000, 124999),
            ('Prosperous ($125,000 to $149,999)', 125000, 149999),
            ('Wealthy ($150,000 to $199,999)', 150000, 199999),
            ('Affluent ($200,000 or more)', 200000, float('inf'))
        ]

        for level, low, high in income_levels:
            if min_income >= low and (max_income is None or max_income <= high):
                filters['income_level'] = level
                break

    return filters

def generate_bot_response(user_input, dataframes):
    user_input = user_input.lower()

    # Combine all dataframes
    combined_data = pd.concat(dataframes.values())

    # Extract filters using the combined data
    filters = extract_filters(user_input, combined_data)
    response = ""

    # Debug: Print filters
    st.write("Extracted Filters:", filters)

    # Apply filters to the data
    filtered_data = combined_data.copy()
    if filters['team']:
        filtered_data = filtered_data[filtered_data['Team'] == filters['team']]
    if filters['fandom_level']:
        filtered_data = filtered_data[filtered_data['Fandom Level'] == filters['fandom_level']]
    if filters['league']:
        filtered_data = filtered_data[filtered_data['League'] == filters['league']]
    if filters['race']:
        filtered_data = filtered_data[filtered_data['Race'] == filters['race']]
    if filters['income_level']:
        if filters['income_level'] in filtered_data.columns:
            filtered_data['Total Convertible Fans'] = filtered_data[filters['income_level']]
        else:
            filtered_data['Total Convertible Fans'] = 0

    # Debug: Print filtered data
    st.write("Filtered Data:", filtered_data)

    if not filtered_data.empty:
        # Construct response with insights
        response_parts = []
        if filters['team']:
            response_parts.append(f"team {filters['team']}")
        if filters['fandom_level']:
            response_parts.append(f"fandom level {filters['fandom_level']}")
        if filters['league']:
            response_parts.append(f"league {filters['league']}")
        if filters['race']:
            response_parts.append(f"race {filters['race']}")
        if filters['income_level']:
            response_parts.append(f"income level {filters['income_level']}")

        response_detail = f"for {' and '.join(response_parts)}: \n"
        response_detail += str(filtered_data.to_dict(orient='records'))
        response = (
            f"Here's a fascinating insight for you: {response_detail}. "
            "Isn't it intriguing how data can reveal such stories? Let's dive deeper or explore another query!"
        )
    else:
        response = (
            "It seems we don't have data that matches your query. However, don't be discouraged! "
            "Try adjusting your filters or ask about another team or demographic. There's always more to uncover in the world of data!"
        )

    return response

def app(dataframes):
    st.header("Chat with our Data Strategist")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User input text box
    user_input = st.text_input("Ask something about the data:")

    if user_input:
        # Generate bot response
        response = generate_bot_response(user_input, dataframes)
        
        # Add user and bot messages to chat history
        st.session_state.chat_history.append({"message": user_input, "is_user": True})
        st.session_state.chat_history.append({"message": response, "is_user": False})

    # Display chat history
    for chat in st.session_state.chat_history:
        message(chat['message'], is_user=chat['is_user'])
