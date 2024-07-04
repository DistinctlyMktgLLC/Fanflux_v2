import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium
from folium.plugins import MarkerCluster

def display_scorecards(df, income_levels):
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

    # Calculate the sum of income columns for each fandom level
    income_sum_avid = df[df['Fandom Level'] == 'Avid'][income_levels].sum().sum()
    income_sum_casual = df[df['Fandom Level'] == 'Casual'][income_levels].sum().sum()
    income_sum_convertible = df[df['Fandom Level'] == 'Convertible Fans'][income_levels].sum().sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="scorecard-avid"><h3>Avid Fans</h3><div class="value">{income_sum_avid}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="scorecard-casual"><h3>Casual Fans</h3><div class="value">{income_sum_casual}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="scorecard-convertible"><h3>Convertible Fans</h3><div class="value">{income_sum_convertible}</div></div>', unsafe_allow_html=True)

def display_table(df):
    columns_to_show = [
        'Team', 'League', 'Neighborhood', 'zipcode', 'Fandom Level',
        'Race', 'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
        'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
        'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
        'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
        'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
        'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
    ]
    df['zipcode'] = df['zipcode'].astype(str).str.zfill(5)
    df_to_show = df[columns_to_show]
    st.dataframe(df_to_show)

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
                
                income_levels = '<br>'.join(
                    [f'{col}: {row[col]}' for col in row.index 
                     if col.startswith(('Struggling', 'Getting', 'Starting', 'Middle', 'Comfortable', 'Doing', 'Prosperous', 'Wealthy', 'Affluent')) 
                     and row[col] > 0]
                )
                
                tooltip_text = (
                    f"Team: {row['Team']}<br>"
                    f"League: {row['League']}<br>"
                    f"City: {row['Neighborhood']}<br>"
                    f"Fandom Level: {row['Fandom Level']}<br>"
                    f"Income Levels:<br>{income_levels}"
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

    # Display scorecards
    display_scorecards(filtered_df, income_levels)

    # Display table
    display_table(filtered_df)

    # Display interactive map
    interactive_map(filtered_df)

if __name__ == "__main__":
    app()
