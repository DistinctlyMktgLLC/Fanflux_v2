import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import leafmap.foliumap as leafmap
import utils

# Load data dynamically based on the page name
df = utils.load_data("White")

def app():
    utils.apply_common_styles()

    st.title("White Baseball Fans")
    
    # Filters
    teams = st.multiselect('Select a Team', options=df['Team'].unique())
    leagues = st.multiselect('Select a League', options=df['League'].unique())
    income_levels = st.multiselect('Select Income Levels', options=df.columns[6:])
    fandom_levels = st.multiselect('Select a Fandom Level', options=df['Fandom Level'].unique())

    filtered_df = df
    if teams:
        filtered_df = filtered_df[filtered_df['Team'].isin(teams)]
    if leagues:
        filtered_df = filtered_df[filtered_df['League'].isin(leagues)]
    if fandom_levels:
        filtered_df = filtered_df[filtered_df['Fandom Level'].isin(fandom_levels)]
    
    if income_levels:
        filtered_df = filtered_df[['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race'] + income_levels]

    # Scorecards
    avid_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Avid'])
    casual_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Casual'])
    convertible_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Convertible Fans'])
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
            <div style="background: #FFD700; padding: 10px; border-radius: 5px;">
                <h3>Avid Fans</h3>
                <p>{avid_fans}</p>
            </div>
            <div style="background: #ADFF2F; padding: 10px; border-radius: 5px;">
                <h3>Casual Fans</h3>
                <p>{casual_fans}</p>
            </div>
            <div style="background: #FF6347; padding: 10px; border-radius: 5px;">
                <h3>Convertible Fans</h3>
                <p>{convertible_fans}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # AgGrid table
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_pagination()
    gb.configure_column('zipcode', type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'], precision=0)
    gb.configure_columns(list(filtered_df.columns[7:]), hide=True)
    grid_options = gb.build()
    
    AgGrid(filtered_df, grid_options=grid_options, enable_enterprise_modules=True)

    # Map
    st.markdown("<h3 style='margin-top: 20px;'>Interactive Map</h3>", unsafe_allow_html=True)
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=False, minimap_control=True
    )

    # Add color-coded markers
    for _, row in filtered_df.iterrows():
        color = 'green' if row['Fandom Level'] == 'Avid' else 'blue' if row['Fandom Level'] == 'Casual' else 'red'
        tooltip = (
            f"Neighborhood: {row['Neighborhood']}<br>"
            f"Race: {row['Race']}<br>"
            f"Team: {row['Team']}<br>"
            f"League: {row['League']}<br>"
            f"Fandom Level: {row['Fandom Level']}<br>"
            f"Total Fans: {row[['Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)', 'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)', 'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)']].sum()}"
        )
        m.add_marker(location=[row['US lat'], row['US lon']], popup=tooltip, icon="info-sign", color=color)

    m.to_streamlit(height=600)
