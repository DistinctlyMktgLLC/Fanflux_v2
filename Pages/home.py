import streamlit as st

def app():
    st.title("Welcome to Fanflux")

    st.markdown("""
    <style>
        .main {
            background-color: #262730;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Dive into the Metrics that Matter")
    st.markdown("""
    - Discover Fan Distribution: Visualize the geographical spread of different fan types.
    - Analyze Fan Intensity: Understand how passionate fans are about their teams.
    - Uncover Economic Insights: See how income levels correlate with fan engagement.
    """)

    st.subheader("Why It's Important")
    st.markdown("""
    - Target Marketing Efforts: Focus your campaigns where they'll have the most impact.
    - Boost Fan Engagement: Tailor your strategies to convert casual fans into avid supporters.
    - Optimize Merchandising: Stock the right products in the right places based on fan demographics.
    """)

    st.subheader("Partnered with DonnLynn Partners")
    st.markdown("""
    We are proud to collaborate with DonnLynn Partners, who brought us this innovative idea. Combined with our data and tech expertise, we have brought Fanflux to life. Together, we have transformed the way you understand and engage with sports fans.

    Ready to transform your understanding of the sports fan landscape? Let's get started!
    """)
