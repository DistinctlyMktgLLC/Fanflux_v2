import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium
from streamlit_folium import st_folium
from st_aggrid import AgGrid, GridOptionsBuilder

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
    df = load_data('data/Fanflux_Intensity_MLB_AAPI.parquet')

    if df.empty:
        return

    # Sidebar filters
    teams = df['Team'].unique().tolist() if 'Team' in df.columns else []
    leagues = df['League'].unique().tolist() if 'League' in df.columns else []
    zipcodes = df['zipcode'].unique().tolist() if 'zipcode' in df.columns else []
    fandom_levels = df['Fandom Level'].unique().tolist() if 'Fandom Level' in df.columns else []

    selected_team = st.sidebar.selectbox("Select a Team", ["All"] + teams)
    selected_league = st.sidebar.selectbox("Select a League", ["All"] + leagues)
    selected_zipcode = st.sidebar.selectbox("Select a Zipcode", ["All"] + zipcodes)
    selected_fandom_level = st.sidebar.selectbox("Select a Fandom Level", ["All"] + fandom_levels)

    # Apply filters
    if selected_team != "All" and 'Team' in df.columns:
        df = df[df['Team'] == selected_team]
    if selected_league != "All" and 'League' in df.columns:
        df = df[df['League'] == selected_league]
    if selected_zipcode != "All" and 'zipcode' in df.columns:
        df = df[df['zipcode'] == selected_zipcode]
    if selected_fandom_level != "All" and 'Fandom Level' in df.columns:
        df = df[df['Fandom Level'] == selected_fandom_level]

    # Calculate Total Fans
    income_cols = [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
        'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
        'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
        'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
        'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
        'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
    ]
    existing_income_cols = [col for col in income_cols if col in df.columns]

    if existing_income_cols:
        df['Total Fans'] = df[existing_income_cols].sum(axis=1)
    else:
        df['Total Fans'] = 0

    # Display data
    st.title("MLB AAPI Fans")

    # Scorecards
    total_fans = df['Total Fans'].sum()
    avg_intensity = df['Intensity'].mean()
    num_teams = df['Team'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Fans", value=f"{total_fans:,}")
    col2.metric(label="Average Intensity", value=f"{avg_intensity:.2f}")
    col3.metric(label="Number of Teams", value=num_teams)

    # Ensure the necessary columns are in the dataframe before displaying
    columns_to_display = ['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race',
                          'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
                          'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
                          'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
                          'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
                          'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
                          'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
                          'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
                          'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)']

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
    st.title("Interactive Map")

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
        if 'US lat' in df.columns and 'US lon' in df.columns:
            for idx, row in df.iterrows():
                tooltip_text = (f"Neighborhood: {row['Neighborhood']}<br>"
                                f"Race: {row['Race']}<br>"
                                f"Team: {row['Team']}<br>"
                                f"League: {row['League']}<br>"
                                f"Fandom Level: {row['Fandom Level']}<br>"
                                f"Total Fans: {row['Total Fans']}")
                folium.Marker([row['US lat'], row['US lon']], 
                              popup=tooltip_text).add_to(m)
        else:
            st.warning("Latitude and Longitude data not available for map visualization.")

        m.to_streamlit(height=700)

if __name__ == "__main__":
    app()
