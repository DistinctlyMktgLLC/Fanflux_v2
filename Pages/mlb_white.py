import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Hide export buttons
hide_export_buttons = """
    <style>
    .stActionButton {display: none;}
    .ag-header-row .ag-header-cell-menu-button {display: none;}
    </style>
"""
st.markdown(hide_export_buttons, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_parquet('data/Fanflux_Intensity_MLB_White.parquet')
    return df

df = load_data()

def app():
    st.title("White Baseball Fans")

    # Sidebar filters
    fandom_level = st.sidebar.multiselect('Select Fandom Level', df['Fandom Level'].unique())
    race = st.sidebar.multiselect('Select Race', df['Race'].unique())
    income_levels = st.sidebar.multiselect('Select Income Levels', df.columns[8:])  # Assuming income levels start from the 9th column
    teams = st.sidebar.multiselect('Select Teams', df['Team'].unique())

    # Calculate totals for scorecards
    total_avid = df[df['Fandom Level'] == 'Avid'][income_levels].sum().sum() if not df[df['Fandom Level'] == 'Avid'][income_levels].empty else 0
    total_casual = df[df['Fandom Level'] == 'Casual'][income_levels].sum().sum() if not df[df['Fandom Level'] == 'Casual'][income_levels].empty else 0
    total_convertible = df[df['Fandom Level'] == 'Convertible Fans'][income_levels].sum().sum() if not df[df['Fandom Level'] == 'Convertible Fans'][income_levels].empty else 0

    st.markdown(f"""
    <div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
        <div style="background-color: #ff6347; padding: 20px; border-radius: 10px; width: 30%; text-align: center;">
            <h2 style="color: white;">Avid Fans</h2>
            <p style="color: white; font-size: 24px;">{total_avid}</p>
        </div>
        <div style="background-color: #ffa500; padding: 20px; border-radius: 10px; width: 30%; text-align: center;">
            <h2 style="color: white;">Casual Fans</h2>
            <p style="color: white; font-size: 24px;">{total_casual}</p>
        </div>
        <div style="background-color: #1e90ff; padding: 20px; border-radius: 10px; width: 30%; text-align: center;">
            <h2 style="color: white;">Convertible Fans</h2>
            <p style="color: white; font-size: 24px;">{total_convertible}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Map
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=2)
    for _, row in df.iterrows():
        color = "blue" if row['Fandom Level'] == "Avid" else "orange" if row['Fandom Level'] == "Casual" else "lightblue"
        folium.Marker(
            location=[row['US lat'], row['US lon']],
            popup=f"Team: {row['Team']}, League: {row['League']}, City: {row['City']}, Fandom Level: {row['Fandom Level']}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    st.write("Fan Locations Map:")
    st_folium(m, width=700, height=500)

app()
