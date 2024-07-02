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
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def generate_scorecards(avid_fans, casual_fans, not_at_all_fans):
    scorecard_html = f"""
    <div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; width: 30%; text-align: center; border-left: 10px solid #005f99; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h3 style="color: #007acc;">Avid Fans</h3>
            <p style="font-size: 24px; color: black;">{avid_fans:,}</p>
        </div>
        <div style="background-color: #fdf0e6; padding: 20px; border-radius: 10px; width: 30%; text-align: center; border-left: 10px solid #e68a00; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h3 style="color: #ffac41;">Casual Fans</h3>
            <p style="font-size: 24px; color: black;">{casual_fans:,}</p>
        </div>
        <div style="background-color: #ffe6e6; padding: 20px; border-radius: 10px; width: 30%; text-align: center; border-left: 10px solid #cc3300; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h3 style="color: #e60000;">Not at all Fans</h3>
            <p style="font-size: 24px; color: black;">{not_at_all_fans:,}</p>
        </div>
    </div>
    """
    st.markdown(scorecard_html, unsafe_allow_html=True)
