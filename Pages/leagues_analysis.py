import streamlit as st
import leafmap.foliumap as leafmap
import polars as pl

# Load the data
@st.cache_data
def load_data():
    return pl.read_parquet('data/combined_leagues.parquet')

df = load_data().to_pandas()

# Main app function for leagues analysis
def app():
    st.title("Leagues Analysis")

    # Filters
    st.sidebar.header("Filters")
    selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique(), key="fandom_level_filter_unique")
    selected_races = st.sidebar.multiselect("Select Race", df['Race'].unique(), key="race_filter_unique")
    selected_leagues = st.sidebar.multiselect("Select League", df['League'].unique(), key="league_filter_unique")
    selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique(), key="team_filter_unique")
    selected_income_levels = st.sidebar.multiselect("Select Income Level", df.columns[12:], key="income_level_filter_unique")

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
    
    # Calculate totals
    total_avid_fans = int(filtered_df[filtered_df['Fandom Level'] == 'Avid'][selected_income_levels].sum().sum())
    total_casual_fans = int(filtered_df[filtered_df['Fandom Level'] == 'Casual'][selected_income_levels].sum().sum())
    total_convertible_fans = int(filtered_df[filtered_df['Fandom Level'] == 'Convertible'][selected_income_levels].sum().sum())

    # Display metrics in scorecards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Avid Fans", value=total_avid_fans)
    with col2:
        st.metric(label="Total Casual Fans", value=total_casual_fans)
    with col3:
        st.metric(label="Total Convertible Fans", value=total_convertible_fans)

    # Create the map with marker clustering
    st.subheader("Fan Opportunity Map")
    with st.spinner("Finding Fandom..."):
        m = leafmap.Map(center=[40, -100], zoom=4, draw_export=False)
        m.add_points_from_xy(
            filtered_df,
            x="US lon",
            y="US lat",
            color_column="Fandom Level",
            popup=["Team", "League", "Fandom Level", "Race"] + selected_income_levels,
            icon_names=["gear", "map", "leaf", "globe"],
            spin=True,
            add_legend=True,
        )
        m.to_streamlit(height=700)

if __name__ == "__main__":
    app()
