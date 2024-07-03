import streamlit as st
import utils

def app():
    st.title("Welcome to Fanflux")
    utils.apply_common_styles()
    
    st.markdown(
        """
        ### Dive into the Metrics that Matter

        Ever wondered why certain fans are more dedicated than others? Or why some regions have higher concentrations of specific fan types? Welcome to Fanflux, where data meets fandom in the most intriguing ways. Here’s what you’ll get:

        - **Discover Fan Distribution:** Visualize the geographical spread of different fan types.
        - **Analyze Fan Intensity:** Understand how passionate fans are about their teams.
        - **Uncover Economic Insights:** See how income levels correlate with fan engagement.

        ### Why It’s Important

        Sports teams, marketers, and fan clubs alike can leverage these insights to:

        - **Target Marketing Efforts:** Focus your campaigns where they’ll have the most impact.
        - **Boost Fan Engagement:** Tailor your strategies to convert casual fans into avid supporters.
        - **Optimize Merchandising:** Stock the right products in the right places based on fan demographics.

        ### What You’ll Get

        - **Interactive Maps:** Dive into detailed visualizations of fan distributions.
        - **Dynamic Charts:** Track trends and analyze data with ease.
        - **Comprehensive Reports:** Generate insights that drive your strategies forward.

        ### Partnered with DonnLynn Partners

        We are proud to collaborate with DonnLynn Partners, who brought us this innovative idea. Combined with our data and tech expertise, has brought Fanflux to life. Together, we are transforming the way you understand and engage with sports fans. 

        Ready to transform your understanding of the sports fan landscape? Let’s get started!

        For more details, contact us at [email@example.com](mailto:email@example.com).
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    app()
