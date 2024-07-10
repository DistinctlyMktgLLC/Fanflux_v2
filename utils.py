# utils.py
import streamlit as st

def display_fan_demographics(df):
    income_columns = [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
        'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
        'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
        'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
        'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
        'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
    ]

    # Calculate the total sums for each fandom level
    total_avid_fans = df[df['Fandom Level'] == 'Avid'][income_columns].sum().sum()
    total_casual_fans = df[df['Fandom Level'] == 'Casual'][income_columns].sum().sum()
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible'][income_columns].sum().sum()

    st.markdown("""
    <style>
        .card {
            padding: 20px;
            margin: 10px;
            background-color: #333;
            color: white;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
        }
        .card h3 {
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='card'><h3>Total Avid Fans</h3><p>{total_avid_fans}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card'><h3>Total Casual Fans</h3><p>{total_casual_fans}</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card'><h3>Total Convertible Fans</h3><p>{total_convertible_fans}</p></div>", unsafe_allow_html=True)
