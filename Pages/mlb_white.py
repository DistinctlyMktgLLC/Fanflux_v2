import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import leafmap.foliumap as leafmap
import folium
from folium.plugins import MarkerCluster

def display_scorecards(df):
    st.markdown(
        """
        <style>
        .scorecard {
            background-color: #000000; /* Black background */
            color: #ffffff; /* White font color */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.5);
            margin: 10px;
            text-align: center;
            position: relative; /* For the left highlight */
        }
        .scorecard h3 {
            margin: 0;
            font-size: 24px;
            color: #ffffff; /* White font color for the title */
        }
        .scorecard .value {
            font-size: 48px;
            color: #ffffff; /* White font color for the numbers */
        }
        .scorecard::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 10px;
            height: 100%;
            background-color: #3498db; /* Pop of color on the left side */
            border-radius: 10px 0 0 10px; /* Rounded left side */
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    avid_count = df[df['Fandom Level'] == 'Avid'].shape[0]
    casual_count = df[df['Fandom Level'] == 'Casual'].shape[0]
    convertible_count = df[df['Fandom Level'] == 'Convertible'].shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="scorecard"><h3>Avid Fans</h3><div class="value">{avid_count}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="scorecard"><h3>Casual Fans</h3><div class="value">{casual_count}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="scorecard"><h3>Convertible Fans</h3><div class="value">{convertible_count}</div></div>', unsafe_allow_html=True)

def display_table(df, page, page_size):
    start = page * page_size
    end = start + page_size
    grid_options = {
        'defaultColDef': {
            'sortable': True,
            'filter': True,
            'resizable': True,
            'floatingFilter': True,
        },
        'domLayout': 'autoHeight',
        'pagination': True,
        'paginationPageSize': page_size,
    }
    AgGrid(df.iloc[start:end], gridOptions=grid_options, height=400, width='100%', theme='streamlit', fit_columns_on_grid_load=True)

def interactive_map(df):
    col1, col2 = st.columns([4, 1])
    options = list(leafmap.basemaps.keys())
    index = options.index("OpenTopoMap")

    with col2:
        basemap = st.selectbox("Select a basemap:", options, index)
    with col1:
        m = leafmap.Map(
            locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
        )
        m.add_basemap(basemap)
        
        # Clustering with correct column names
        if 'US lat' in df.columns and 'US lon' in df.columns:
            marker_cluster = MarkerCluster().add_to(m)
            for lat, lon in zip(df['US lat'], df['US lon']):
                folium.Marker(location=[lat, lon]).add_to(marker_cluster)
        
        m.to_streamlit(height=700)

def app():
    st.title("White Baseball Fans")

    # Load data
    df = pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")

    if df.empty:
        st.error("No data available.")
        return

    # Display scorecards
    display_scorecards(df)

    # Pagination controls
    total_records = df.shape[0]
    page_size = 50  # Number of records per page
    total_pages = (total_records // page_size) + 1
    page = st.slider('Page', 0, total_pages - 1, 0)

    # Display table with pagination
    display_table(df, page, page_size)

    # Display interactive map
    interactive_map(df)

if __name__ == "__main__":
    app()
