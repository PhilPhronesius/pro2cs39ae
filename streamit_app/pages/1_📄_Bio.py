import streamlit as st
from pathlib import Path
from PIL import Image, ImageOps

st.title("Bio Page")

# ---------- TODO: Replace with your own info ----------
st.markdown("""
I am a student with a strong interest in educational data and higher education trends. 
My work focuses on understanding patterns in college rankings, tuition costs, and enrollment metrics. 
I use Python, Pandas, and Plotly to extract insights and create interactive visualizations. 
Streamlit allows me to turn data into accessible dashboards for both academic and professional audiences. 
My goal is to help people make data-informed decisions and uncover meaningful trends in large datasets.
""")

# Highlights
st.markdown("### Highlights")
highlights = [
    "Analyzed US college ranking datasets (2022USCollegeRankings.csv)",
    "Used Python, Pandas, Plotly, and Streamlit for data analysis and visualization",
    "Created interactive charts to explore tuition, enrollment, and rankings",
    "Focused on understanding the impact of geography on college rankings",
    "Learned to present insights in a clear and accessible way"
]
for h in highlights:
    st.write(f"- {h}")

# Visualization philosophy
st.markdown("### Visualization Philosophy")
st.markdown("""
I aim to make visualizations that are clear, easy to interpret, and ethically accurate. 
Charts should help users explore the data without misrepresenting it. 
Accessibility and clarity are important so that insights are understandable to everyone.
""")
