import streamlit as st
from pathlib import Path
from PIL import Image, ImageOps

st.title("Bio Page")

# ---------- TODO: Replace with your own info ----------
st.markdown("""
I am a data analyst with a strong interest in educational data and higher education trends. 
My work focuses on understanding patterns in college rankings, tuition costs, and enrollment metrics. 
I use Python, Pandas, and Plotly to extract insights and create interactive visualizations. 
Streamlit allows me to turn data into accessible dashboards for both academic and professional audiences. 
My goal is to help people make data-informed decisions and uncover meaningful trends in large datasets.
""")

# Highlights
st.markdown("### Highlights")
highlights = [
    "Completed coursework in Data Analysis and Visualization",
    "Skilled in Python, Pandas, and NumPy for data processing",
    "Created interactive dashboards using Plotly and Streamlit",
    "Analyzed higher education datasets, including US college rankings",
    "Strong focus on data clarity, accessibility, and ethical use"
]
for h in highlights:
    st.write(f"- {h}")

# Visualization philosophy
st.markdown("### Visualization Philosophy")
st.markdown("""
I prioritize clarity, accessibility, and ethical use in all visualizations. 
Each chart should communicate the story in an intuitive way, be accessible to all users, 
and accurately represent the underlying data without bias. 
Interactive dashboards help users explore insights while maintaining transparency and trust.
""")
