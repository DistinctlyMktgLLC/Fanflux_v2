import streamlit as st
import pandas as pd
import plotly.express as px
import leafmap.foliumap as leafmap

def display_scorecards(df):
    total_avid = df[df['Fandom Level'] == 'Avid']['Total'].sum()
    total_casual = df[df['Fandom Level'] == 'Casual']['Total'].sum()
    total_convertible = df[df['Fandom Level'] == 'Convertible Fans']['Total'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='scorecard' style='background-color:#FF6347;'><h2>Avid Fans</h2><h1>{total_avid}</h1></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='scorecard' style='background-color:#FFA500;'><h2>Casual Fans</h2><h1>{total_casual}</h1></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='scorecard' style='background-color:#1E90FF;'><h2>Convertible Fans</h2><h1>{total_convertible}</h1></div>", unsafe_allow_html=True)

def display_table(df):
    styled_df = df.style.set_properties(**{'text-align': 'center'}).hide_index()
    st.dataframe(styled_df)

def display_map(df):
    m = leafmap.Map(center=[40, -100], zoom=4)
    for _, row in df.iterrows():
        m.add_marker([row['US lat'], row['US lon']], popup=f"Team: {row['Team']}, League: {row['League']}, City: {row['Neighborhood']}, Fandom Level: {row['Fandom Level']}")
    m.to_streamlit(width=700, height=500)

def app():
    st.title("White Baseball Fans")

    data_path = 'data/Fanflux_Intensity_MLB_White.csv'
    df = pd.read_csv(data_path)

    df['Total'] = df.iloc[:, 14:].sum(axis=1)
    df['zipcode'] = df['zipcode'].astype(str).str.zfill(5)

    fandom_levels = df['Fandom Level'].unique()
    races = df['Race'].unique()
    income_levels = df.columns[14:]

    selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", fandom_levels)
    selected_races = st.sidebar.multiselect("Select Race", races)
    selected_income_levels = st.sidebar.multiselect("Select Income Levels", income_levels)
    selected_teams = st.sidebar.multiselect("Select Teams", df['Team'].unique())

    filtered_df = df[
        (df['Fandom Level'].isin(selected_fandom_levels)) &
        (df['Race'].isin(selected_races)) &
        (df[selected_income_levels].sum(axis=1) > 0) &
        (df['Team'].isin(selected_teams))
    ]

    display_scorecards(filtered_df)
    display_table(filtered_df)
    display_map(filtered_df)
