import streamlit as st

def app():
    st.title("Welcome to Fanflux")
    st.write("Explore Key Insights")

    st.markdown("""
    <style>
        .main {
            background-color: #262730;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Explore Key Insights")
    st.markdown("""
    - See Where Fans Are: Visualize where different types of fans are located.
    - Measure Fan Passion: Understand how dedicated fans are to their teams.
    - Economic Insights: Learn how income levels relate to fan engagement.
    """)

    st.subheader("Why Fanflux Matters")
    st.markdown("""
    - Smart Marketing: Focus your campaigns on the areas that will have the most impact.
    - Increase Engagement: Find ways to turn casual fans into passionate supporters.
    - Better Merchandising: Ensure you have the right products in the right places for your fans.
    """)

    st.subheader("Partnered with DonnLynn Partners")
    st.markdown("""
    We are proud to collaborate with DonnLynn Partners, who brought us this innovative idea. Combined with our data and tech expertise, we have brought Fanflux to life. Together, we have transformed the way you understand and engage with sports fans.

    Ready to transform your understanding of the sports fan landscape? Let's get started!
    """)

# Ensure the app function is only called if this script is run directly
if __name__ == "__main__":
    app()