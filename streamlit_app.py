import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title="Fanflux Intensity Finder", page_icon="🏆")

# Show the page title and description
st.title("🏆 Find Fans")
st.write(
    """
    Fanflux visualizes Fan data from our Database that shows where fans live, how much they 
    make and their team and league preferences. Just click on the widgets below to explore!
    """
)

# Load data from CSV files
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load the intensity data
intensity_data = load_data('data/Intensity_MLB_ALLRaces.csv')

# Identify income level columns
income_columns = [
    'Struggling (Less than $10,000)',
    'Getting By ($10,000 to $14,999)',
    'Getting By ($15,000 to $19,999)',
    'Starting Out ($20,000 to $24,999)',
    'Starting Out ($25,000 to $29,999)',
    'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)',
    'Middle Class ($40,000 to $44,999)',
    'Middle Class ($45,000 to $49,999)',
    'Comfortable ($50,000 to $59,999)',
    'Comfortable ($60,000 to $74,999)',
    'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)',
    'Prosperous ($125,000 to $149,999)',
    'Wealthy ($150,000 to $199,999)',
    'Affluent ($200,000 or more)'
]

# Show multiselect widget for teams
teams = st.multiselect(
    "Teams",
    intensity_data['Team'].unique(),
    intensity_data['Team'].unique()
)

# Show multiselect widget for leagues
leagues = st.multiselect(
    "Leagues",
    intensity_data['League'].unique(),
    intensity_data['League'].unique()
)

# Show multiselect widget for races
races = st.multiselect(
    "Race",
    intensity_data['Race'].unique(),
    intensity_data['Race'].unique()
)

# Show slider widget for intensity
intensity = st.slider("Intensity", 0, 100, (0, 100))

# Filter data based on widget input
@st.cache_data
def filter_data(data, teams, leagues, races, intensity_range):
    return data[
        (data["Team"].isin(teams)) & 
        (data["League"].isin(leagues)) &
        (data["Race"].isin(races)) &
        (data["Dispersion Score"].between(intensity_range[0], intensity_range[1]))
    ]

df_filtered = filter_data(intensity_data, teams, leagues, races, intensity)

# Calculate metrics
@st.cache_data
def calculate_metrics(filtered_data, income_cols):
    average_intensity = filtered_data["Dispersion Score"].mean()
    race_totals = {}
    for race in filtered_data["Race"].unique():
        race_data = filtered_data[filtered_data["Race"] == race]
        total_people = race_data[income_cols].sum().sum()
        race_totals[race] = total_people
    return average_intensity, race_totals

average_intensity, race_totals = calculate_metrics(df_filtered, income_columns)

# Create a pie chart for race distribution
race_totals_df = pd.DataFrame(list(race_totals.items()), columns=['Race', 'Total'])
pie_chart = alt.Chart(race_totals_df).mark_arc().encode(
    theta=alt.Theta(field="Total", type="quantitative"),
    color=alt.Color(field="Race", type="nominal")
).properties(title="Race Distribution")

# Display the pie chart
st.write("## Race Distribution")
st.altair_chart(pie_chart, use_container_width=True)

# Display the filtered data as a table
st.write("## Filtered Data Table")
st.dataframe(df_filtered)
