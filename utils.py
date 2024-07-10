import streamlit as st

def display_fan_demographics(df):
    # Summing the values for each fandom level
    total_avid_fans = df[df['Fandom Level'] == 'Avid'].shape[0]
    total_casual_fans = df[df['Fandom Level'] == 'Casual'].shape[0]
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible'].shape[0]

    # Creating scorecards with a visual border and color accent
    st.markdown(f"""
        <div style="border-left: 5px solid #4CAF50; padding: 10px; margin: 10px 0;">
            <h3>Total Avid Fans</h3>
            <p style="font-size: 24px;">{total_avid_fans}</p>
        </div>
        <div style="border-left: 5px solid #FFC107; padding: 10px; margin: 10px 0;">
            <h3>Total Casual Fans</h3>
            <p style="font-size: 24px;">{total_casual_fans}</p>
        </div>
        <div style="border-left: 5px solid #F44336; padding: 10px; margin: 10px 0;">
            <h3>Total Convertible Fans</h3>
            <p style="font-size: 24px;">{total_convertible_fans}</p>
        </div>
    """, unsafe_allow_html=True)
