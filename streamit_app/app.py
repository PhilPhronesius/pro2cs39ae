# app.py
import streamlit as st

# Page setup
st.set_page_config(
    page_title="US College Rankings Dashboard",
    page_icon="🎓",
    layout="wide"
)

# App title
st.title("🎓 U.S. College Rankings & Tuition Dashboard")
st.markdown("Welcome to the multi-page Streamlit app analyzing college rankings, tuition, enrollment, and geography.")

# Intro text
st.markdown("""
This dashboard is divided into several sections:

- **Bio:** Learn about the project, dataset, and research questions.  
- **Charts Gallery:** Visual insights using bar charts, line charts, and donut charts.  
- **Dashboard:** Interactive analysis including the U.S. choropleth map.  
- **Future Work:** Planned extensions and ideas for improvement.

""")

st.info("👈 Use the sidebar on the left to navigate between pages.")
