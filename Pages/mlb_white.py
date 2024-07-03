import streamlit as st
import utils
import folium

# Load data
df = utils.load_data('White')

def app():
    st.title("White Baseball Fans")

    avid_fans = df[df['Fandom Level'] == 'Avid'].shape[0]
    casual_fans = df[df['Fandom Level'] == 'Casual'].shape[0]
    convertible_fans = df[df['Fandom Level'] == 'Not at all'].shape[0]

    scorecard_style = """
    <style>
    .scorecard {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: black;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
    }
    .scorecard .highlight {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 10px;
        border-radius: 10px 0 0 10px;
    }
    </style>
    """

    st.markdown(scorecard_style, unsafe_allow_html=True)

    def render_scorecard(color, title, value):
        card_html = f"""
        <div class="scorecard">
            <div class="highlight" style="background-color: {color};"></div>
            <div>
                <h2>{title}</h2>
                <p style="font-size: 24px;">{value}</p>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        render_scorecard('green', 'Avid Fans', avid_fans)
    with col2:
        render_scorecard('blue', 'Casual Fans', casual_fans)
    with col3:
        render_scorecard('red', 'Convertible Fans', convertible_fans)

    # Sidebar filters
    st.sidebar.header("Filters")
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    league = st.sidebar.selectbox('Select a League', ['Choose an option'] + sorted(df['League'].unique()))
    income_level = st.sidebar.selectbox('Select Income Levels', ['Choose an option'] + df.columns[14:].tolist())
    fandom_level = st.sidebar.selectbox('Select a Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))

    filtered_df = df.copy()

    if team != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Team'] == team]

    if league != 'Choose an option':
        filtered_df = filtered_df[filtered_df['League'] == league]

    if income_level != 'Choose an option':
        filtered_df = filtered_df[filtered_df[income_level] > 0]

    if fandom_level != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Fandom Level'] == fandom_level]

    # Render AgGrid
    st.subheader("Fan Opportunity Data")
    utils.render_aggrid(filtered_df)

    # Render map
    st.subheader("Fan Opportunity Map")
    basemap = st.sidebar.selectbox("Select a basemap:", options=['OpenStreetMap', 'Stamen Toner', 'Stamen Terrain', 'Stamen Watercolor', 'CartoDB positron', 'CartoDB dark_matter'], index=0)
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    folium.TileLayer(basemap).add_to(m)
    utils.add_map_markers(m, filtered_df, 'Fandom Level', {
        'Avid': 'green',
        'Casual': 'blue',
        'Not at all': 'red'
    })
    st.components.v1.html(m._repr_html_(), height=700)

app()
