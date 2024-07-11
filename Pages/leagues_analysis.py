import streamlit as st
import leafmap.foliumap as leafmap
import polars as pl
import pandas as pd

# Load the updated data
@st.cache_data
def load_data():
    df = pl.read_parquet('data/updated_combined_leagues.parquet')
    return df

df = load_data().to_pandas()

# Main app function for leagues analysis
def app():
    st.title("Leagues Analysis")

    # Filters
    st.sidebar.header("Filters")
    selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique(), key="fandom_level_filter_leagues")
    selected_races = st.sidebar.multiselect("Select Race", df['Race'].unique(), key="race_filter_leagues")
    selected_leagues = st.sidebar.multiselect("Select League", df['League'].unique(), key="league_filter_leagues")
    selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique(), key="team_filter_leagues")
    selected_income_levels = st.sidebar.multiselect("Select Income Level", df.columns[12:], key="income_level_filter_leagues")

    # Apply filters
    filtered_df = df.copy()
    if selected_fandom_levels:
        filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom_levels)]
    if selected_races:
        filtered_df = filtered_df[filtered_df['Race'].isin(selected_races)]
    if selected_leagues:
        filtered_df = filtered_df[filtered_df['League'].isin(selected_leagues)]
    if selected_teams:
        filtered_df = filtered_df[filtered_df['Team'].isin(selected_teams)]
    if selected_income_levels:
        filtered_df = filtered_df[filtered_df[selected_income_levels].sum(axis=1) > 0]

    # Calculate metrics
    total_avid_fans = filtered_df[filtered_df['Fandom Level'] == 'Avid']['Total Fans'].sum()
    total_casual_fans = filtered_df[filtered_df['Fandom Level'] == 'Casual']['Total Fans'].sum()
    total_convertible_fans = filtered_df[filtered_df['Fandom Level'] == 'Convertible']['Total Fans'].sum()

    # Display metrics in scorecards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Avid Fans", value=int(total_avid_fans))
    with col2:
        st.metric(label="Total Casual Fans", value=int(total_casual_fans))
    with col3:
        st.metric(label="Total Convertible Fans", value=int(total_convertible_fans))

    # Add explanatory note
    st.markdown("""
        **Note:** The initial data displayed is a 10% sample of the total dataset. Adjusting filters will apply to this sample.
    """)
    
    # Add conditional explanatory note
    if selected_teams and selected_leagues:
        st.markdown("""
            **Additional Note:** The total fans displayed in the scorecards represent the sum of fans for the selected teams and leagues. If both teams and leagues are selected, the total fans will be a combined sum.
        """)

    # Create the map with marker clustering
    st.subheader("Fan Opportunity Map")
    with st.spinner("Finding Fandom..."):
        m = leafmap.Map(center=[40, -100], zoom=4, draw_export=False)
        color_column = "Fandom Level"
        color_map = {
            "Avid": "red",
            "Casual": "blue",
            "Convertible": "green"
        }
        popup = ["Team", "League", "Neighborhood", "Fandom Level", "Race", "Total Fans"]

        m.add_points_from_xy(
            filtered_df,
            x="US lon",
            y="US lat",
            color_column=color_column,
            colors=[color_map[val] for val in filtered_df[color_column].unique()],
            popup=popup,
            min_width=200,
            max_width=300
        )

        m.to_streamlit(width=1200, height=700)

# Run the app function
app()
