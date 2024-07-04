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
        .scorecard-avid {
            background-color: #000000;
            color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.5);
            margin: 10px;
            text-align: center;
            position: relative;
        }
        .scorecard-avid::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 10px;
            height: 100%;
            background-color: #e74c3c;
            border-radius: 10px 0 0 10px;
        }

        .scorecard-casual {
            background-color: #000000;
            color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.5);
            margin: 10px;
            text-align: center;
            position: relative;
        }
        .scorecard-casual::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 10px;
            height: 100%;
            background-color: #f39c12;
            border-radius: 10px 0 0 10px;
        }

        .scorecard-convertible {
            background-color: #000000;
            color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.5);
            margin: 10px;
            text-align: center;
            position: relative;
        }
        .scorecard-convertible::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 10px;
            height: 100%;
            background-color: #3498db;
            border-radius: 10px 0 0 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Filtered counts
    avid_count = df[df['Fandom Level'] == 'Avid'].shape[0]
    casual_count = df[df['Fandom Level'] == 'Casual'].shape[0]
    convertible_count = df[df['Fandom Level'] == 'Convertible Fans'].shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="scorecard-avid"><h3>Avid Fans</h3><div class="value">{avid_count}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="scorecard-casual"><h3>Casual Fans</h3><div class="value">{casual_count}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="scorecard-convertible"><h3>Convertible Fans</h3><div class="value">{convertible_count}</div></div>', unsafe_allow_html=True)

def display_table(df):
    if not df.empty:
        grid_options = {
            'defaultColDef': {
                'sortable': True,
                'filter': True,
                'resizable': True,
                'floatingFilter': True,
            },
            'domLayout': 'autoHeight',
            'pagination': False,
        }
        AgGrid(df, gridOptions=grid_options, height=400, width='100%', theme='streamlit', fit_columns_on_grid_load=True)
    else:
        st.warning("No data available to display.")

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
        
        # Clustering with correct column names and tooltips
        if 'US lat' in df.columns and 'US lon' in df.columns:
            marker_cluster = MarkerCluster().add_to(m)
            for _, row in df.iterrows():
                lat = row['US lat']
                lon = row['US lon']
                fandom_level = row['Fandom Level']
                if fandom_level == 'Avid':
                    color = 'red'
                elif fandom_level == 'Casual':
                    color = 'orange'
                else:
                    color = 'blue'
                tooltip_text = (
                    f"Team: {row['Team']}, League: {row['League']}, City: {row['City']}, "
                    f"Fandom Level: {row['Fandom Level']}, Income Levels: {', '.join([f'{col}: {row[col]}' for col in row.index if col.startswith(('Struggling', 'Getting', 'Starting', 'Middle', 'Comfortable', 'Doing', 'Prosperous', 'Wealthy', 'Affluent')) and row[col] > 0])}"
                )
                folium.Marker(
                    location=[lat, lon],
                    tooltip=tooltip_text,
                    icon=folium.Icon(color=color)
                ).add_to(marker_cluster)
        
        m.to_streamlit(height=700)

def app():
    st.title("White Baseball Fans")

    # Load data
    df = pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")
    
    if df.empty:
        st.error("No data available.")
        return

    # Update "Not at all" to "Convertible Fans"
    df['Fandom Level'] = df['Fandom Level'].replace('Not at all', 'Convertible Fans')

    # Filters
    fandom_levels = df['Fandom Level'].unique().tolist()
    races = df['Race'].unique().tolist()
    income_levels = [col for col in df.columns if col.startswith(('Struggling', 'Getting', 'Starting', 'Middle', 'Comfortable', 'Doing', 'Prosperous', 'Wealthy', 'Affluent'))]
    teams = df['Team'].unique().tolist()

    selected_fandom_levels = st.sidebar.multiselect('Select Fandom Level', fandom_levels)
    selected_races = st.sidebar.multiselect('Select Race', races)
    selected_income_levels = st.sidebar.multiselect('Select Income Levels', income_levels)
    selected_teams = st.sidebar.multiselect('Select Teams', teams)

    # Filter dataframe based on selections
    filtered_df = df[
        (df['Fandom Level'].isin(selected_fandom_levels) if selected_fandom_levels else df['Fandom Level'].notnull()) &
        (df['Race'].isin(selected_races) if selected_races else df['Race'].notnull()) &
        (df[selected_income_levels].sum(axis=1) > 0 if selected_income_levels else df['Fandom Level'].notnull()) &
        (df['Team'].isin(selected_teams) if selected_teams else df['Team'].notnull())
    ]

    # Debugging: Check shape of filtered data and its contents
    st.write("Filtered Data Shape:", filtered_df.shape)
    st.write("Filtered Data Head:", filtered_df.head())

    # Display scorecards
    display_scorecards(filtered_df)

    # Display table
    display_table(filtered_df)

    # Display interactive map
    interactive_map(filtered_df)

if __name__ == "__main__":
    app()
