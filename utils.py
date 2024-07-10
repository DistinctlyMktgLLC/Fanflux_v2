import streamlit as st

def display_fan_demographics(df):
    total_avid_fans = df[df['Fandom Level'] == 'Avid'].shape[0]
    total_casual_fans = df[df['Fandom Level'] == 'Casual'].shape[0]
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible'].shape[0]

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
