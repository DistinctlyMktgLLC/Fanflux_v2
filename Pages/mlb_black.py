import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from st_aggrid import AgGrid, GridOptionsBuilder
import utils

# Load data from Parquet file
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_parquet(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

def app():
    utils.apply_common_styles()

    df = load_data('data/Fanflux_Intensity_MLB_Black.parquet')

    if df.empty:
        return

    # Format the zipcode column as a 5-digit string
    if 'zipcode' in df.columns:
        df['zipcode'] = df['zipcode'].astype(str).str.zfill(5)

    # Sidebar filters
    teams = df['Team'].unique().tolist() if 'Team' in df.columns else []
    leagues = df['League'].unique().tolist() if 'League' in df.columns else []
    zipcodes = df['zipcode'].unique().tolist() if 'zipcode' in df.columns else []
    fandom_levels = df['Fandom Level'].unique().tolist() if 'Fandom Level' in df.columns else []
    income_levels = [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
        'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
        'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
        'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
        'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
        'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
    ]

    selected_teams = st.sidebar.multiselect("Select a Team", teams)
    selected_leagues = st.sidebar.multiselect("Select a League", leagues)
    selected_income_levels = st.sidebar.multiselect("Select an Income Level", income_levels)
    selected_fandom_levels = st.sidebar.multiselect("Select a Fandom Level", fandom_levels)

    # Apply filters
    if selected_teams:
        df = df[df['Team'].isin(selected_teams)]
    if selected_leagues:
        df = df[df['League'].isin(selected_leagues)]
    if selected_fandom_levels:
        df = df[df['Fandom Level'].isin(selected_fandom_levels)]

    # Calculate Total Fans
    df['Total Fans'] = df[selected_income_levels].sum(axis=1) if selected_income_levels else 0

    # Display data
    st.title("Black Baseball Fans")

    # Scorecards
    avid_fans = df[df['Fandom Level'] == 'Avid']['Total Fans'].sum()
    casual_fans = df[df['Fandom Level'] == 'Casual']['Total Fans'].sum()
    not_at_all_fans = df[df['Fandom Level'] == 'Not at all']['Total Fans'].sum()

    utils.generate_scorecards(avid_fans, casual_fans, not_at_all_fans)

    # Ensure the necessary columns are in the dataframe before displaying
    columns_to_display = ['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race'] + selected_income_levels

    existing_columns = [col for col in columns_to_display if col in df.columns]
    missing_columns = set(columns_to_display) - set(existing_columns)

    if missing_columns:
        st.warning(f"The following columns are missing in the dataset: {', '.join(missing_columns)}")

    # Use AgGrid to display the dataframe
    gb = GridOptionsBuilder.from_dataframe(df[existing_columns])
    gb.configure_pagination(paginationPageSize=10)  # Adjust pagination as needed
    gb.configure_default_column(editable=False, sortable=True, filter=True)
    gb.configure_grid_options(domLayout='normal', suppressCsvExport=True, suppressExcelExport=True)  # Disable export
    
    # Customize grid options further
    gb.configure_column("Team", header_name="Team", sortable=True, filter=True, editable=False)
    gb.configure_column("League", header_name="League", sortable=True, filter=True, editable=False)
    gb.configure_column("Neighborhood", header_name="Neighborhood", sortable=True, filter=True, editable=False)
    gb.configure_column("zipcode", header_name="Zipcode", sortable=True, filter=True, editable=False)
    gb.configure_column("Intensity", header_name="Intensity", sortable=True, filter=True, editable=False)
    gb.configure_column("Fandom Level", header_name="Fandom Level", sortable=True, filter=True, editable=False)
    gb.configure_column("Race", header_name="Race", sortable=True, filter=True, editable=False)

    grid_options = gb.build()
    AgGrid(df[existing_columns], gridOptions=grid_options, enable_enterprise_modules=True)

    # Create an interactive map with options
    st.title("Mapping Fandom")

    col1, col2 = st.columns([4, 1])
    options = list(leafmap.basemaps.keys())
    index = options.index("OpenTopoMap")

    with col2:
        basemap = st.selectbox("Select a basemap:", options, index)

    with col1:
        m = leafmap.Map(
            locate_control=True, latlon_control=True, draw_export=False, minimap_control=True  # Disable export
        )
        m.add_basemap(basemap)

        # Add markers from the dataframe
        m = utils.add_markers_to_map(m, df)
        m.to_streamlit(height=700)

if __name__ == "__main__":
    app()
