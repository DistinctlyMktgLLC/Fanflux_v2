# utils.py
import streamlit as st
import folium

def format_tooltip(row):
    return (f"<div style='white-space: nowrap; text-align: left;'>"
            f"<b>Neighborhood:</b> {row['Neighborhood']}<br>"
            f"<b>Race:</b> {row['Race']}<br>"
            f"<b>Team:</b> {row['Team']}<br>"
            f"<b>League:</b> {row['League']}<br>"
            f"<b>Fandom Level:</b> {row['Fandom Level']}<br>"
            f"<b>Total Fans:</b> {row['Total Fans']:,}</div>")

def add_markers_to_map(m, df):
    if 'US lat' in df.columns and 'US lon' in df.columns:
        for idx, row in df.iterrows():
            tooltip_text = format_tooltip(row)
            folium.Marker([row['US lat'], row['US lon']], 
                          popup=folium.Popup(tooltip_text, max_width=300)).add_to(m)
    else:
        st.warning("Latitude and Longitude data not available for map visualization.")
    return m

def apply_common_styles():
    st.markdown(
        """
        <style>
        .main .block-container {
            background-color: black;
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        .hero-section {
            text-align: center;
            padding: 50px;
            background-image: url('https://path/to/your/background/image.jpg');
            background-size: cover;
        }
        .hero-section h1 {
            font-size: 48px;
            margin-bottom: 20px;
        }
        .hero-section p {
            font-size: 24px;
            margin-bottom: 40px;
        }
        .cta-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 20px;
            color: white;
            background-color: #007acc;
            border-radius: 5px;
            text-decoration: none;
        }
        .cta-button:hover {
            background-color: #005f99;
        }
        .features-section {
            display: flex;
            justify-content: space-around;
            margin: 50px 0;
        }
        .feature {
            width: 30%;
            text-align: center;
        }
        .feature h3 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        .feature p {
            font-size: 18px;
        }
        .scorecard {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .scorecard div {
            background-color: #333;
            padding: 20px;
            border-radius: 10px;
            width: 30%;
            text-align: center;
            border-left: 10px solid #005f99;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .scorecard h3 {
            color: #007acc;
        }
        .scorecard p {
            font-size: 24px;
            color: white;
        }
        .footer {
            background-color: #222;
            color: white;
            padding: 20px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def generate_scorecards(avid_fans, casual_fans, not_at_all_fans):
    scorecard_html = f"""
    <div class="scorecard">
        <div style="border-left-color: #005f99;">
            <h3>Avid Fans</h3>
            <p>{avid_fans:,}</p>
        </div>
        <div style="border-left-color: #e68a00;">
            <h3>Casual Fans</h3>
            <p>{casual_fans:,}</p>
        </div>
        <div style="border-left-color: #cc3300;">
            <h3>Not at all Fans</h3>
            <p>{not_at_all_fans:,}</p>
        </div>
    </div>
    """
    st.markdown(scorecard_html, unsafe_allow_html=True)
