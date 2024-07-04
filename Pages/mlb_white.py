import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# Load data
@st.cache
def load_data():
    df = pd.read_parquet('data/Fanflux_Intensity_MLB_White.parquet')
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Fanflux Navigation")
selected_fandom = st.sidebar.multiselect("Select Fandom Level", df["Fandom Level"].unique())
selected_race = st.sidebar.multiselect("Select Race", df["Race"].unique())
selected_income = st.sidebar.multiselect("Select Income Levels", df.columns[7:15])
selected_team = st.sidebar.multiselect("Select Teams", df["Team"].unique())

# Filter data based on selections
filtered_df = df.copy()
if selected_fandom:
    filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom)]
if selected_race:
    filtered_df = filtered_df[filtered_df['Race'].isin(selected_race)]
if selected_income:
    filtered_df = filtered_df.loc[:, ['Team', 'League', 'Neighborhood', 'zipcode', 'Fandom Level', 'Race'] + selected_income]
if selected_team:
    filtered_df = filtered_df[filtered_df['Team'].isin(selected_team)]

# Calculate totals for scorecards
avid_total = filtered_df[filtered_df['Fandom Level'] == 'Avid'].iloc[:, 7:15].sum().sum()
casual_total = filtered_df[filtered_df['Fandom Level'] == 'Casual'].iloc[:, 7:15].sum().sum()
convertible_total = filtered_df[filtered_df['Fandom Level'] == 'Convertible Fans'].iloc[:, 7:15].sum().sum()

# Function to create styled scorecards
def create_scorecard(label, value, color):
    return f"""
    <div style="background-color:{color};padding:10px;border-radius:10px;margin:10px;box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.2);">
        <h3 style="color:white;text-align:center;">{label}</h3>
        <h1 style="color:white;text-align:center;">{value}</h1>
    </div>
    """

# Display scorecards
st.markdown(f"""
<div style="display:flex;justify-content:space-between;">
    {create_scorecard('Avid Fans', avid_total, '#FF5733')}
    {create_scorecard('Casual Fans', casual_total, '#FFC300')}
    {create_scorecard('Convertible Fans', convertible_total, '#3498DB')}
</div>
""", unsafe_allow_html=True)

# Map
st.title("Map of Fans")
m = leafmap.Map(center=[40, -100], zoom=4)
m.add_points_from_xy(filtered_df, x="US lon", y="US lat", color_column="Fandom Level", icon_names=["gear", "map", "leaf", "globe"], spin=True, add_legend=True)
m.to_streamlit(height=700)
