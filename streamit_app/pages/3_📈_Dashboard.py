# pages/3_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ---------------------------
# Page Configuration
st.set_page_config(page_title="US College Dashboard", page_icon="🎓", layout="wide")

st.title("🎓 US College Dashboard")
st.caption("Explore tuition, enrollment, rankings, and regional distribution of US colleges (2022 dataset).")

st.markdown("""
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
""", unsafe_allow_html=True)

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "2022USCollegeRankings.csv")
df = pd.read_csv(csv_path)

df["Tuition"].fillna(df["Tuition"].median(), inplace=True)

# ---------------------------
# Sidebar Filters
st.sidebar.header("Filters")

rank_min, rank_max = int(df["Adjusted Rank"].min()), int(df["Adjusted Rank"].max())
selected_rank = st.sidebar.slider("Rank Range", rank_min, rank_max, (rank_min, rank_max))

tuition_min, tuition_max = int(df["Tuition"].min()), int(df["Tuition"].max())
selected_tuition = st.sidebar.slider("Tuition Range ($)", tuition_min, tuition_max, (tuition_min, tuition_max))

filtered_df = df[
    (df["Tuition"].between(*selected_tuition)) &
    (df["Adjusted Rank"].between(*selected_rank))
]

# ---------------------------
# KPIs
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Colleges", len(filtered_df))
col2.metric("Median Tuition ($)", int(filtered_df["Tuition"].median()))
col3.metric("Median Rank", int(filtered_df["Adjusted Rank"].median()))
col4.metric("Average Enrollment", int(filtered_df["Enrollment Numbers"].median()))

# ---------------------------
# Visual 1: Tuition vs Rank (Scatter Plot)
st.subheader("💰 Tuition vs College Rank")
st.caption("Check whether higher tuition is associated with higher college ranking.")

fig1 = px.scatter(filtered_df, x="Tuition", y="Adjusted Rank", 
                  hover_name="College Name", size="Enrollment Numbers", 
                  title="Tuition vs Adjusted Rank (Interactive)"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# Visual 2: Enrollment Distribution by Rank Tier (Bar Chart)
st.subheader("🏫 Enrollment Distribution by Rank Tier")

# Create Rank Tier column (Top 10, 11-50, 51+)
def rank_tier(rank):
    if rank <= 10:
        return "Top 10"
    elif rank <= 50:
        return "11-50"
    else:
        return "51+"

filtered_df["Rank Tier"] = filtered_df["Adjusted Rank"].apply(rank_tier)

rank_enrollment = filtered_df.groupby("Rank Tier")["Enrollment Numbers"].sum().reset_index()

fig2 = px.bar(rank_enrollment, x="Rank Tier", y="Enrollment Numbers",
              title="Total Enrollment by Rank Tier", labels={"Enrollment Numbers": "Total Enrollment", "Rank Tier": "Rank Tier"}, 
              hover_data=["Enrollment Numbers"], color="Enrollment Numbers",
              color_continuous_scale="Blues"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# Visual 3: Top Colleges by Tuition (Horizontal Bar)
st.subheader("🎓 Top 10 Colleges by Tuition")

top10_tuition = filtered_df.sort_values("Tuition", ascending=False).head(10)

fig3 = px.bar(top10_tuition, x="Tuition", y="College Name", orientation="h", 
              color="Adjusted Rank", color_continuous_scale="Viridis", 
              title="Top 10 Colleges with Highest Tuition", 
              hover_data=["Adjusted Rank", "Enrollment Numbers"]
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# Visual 4: Tuition vs Enrollment (Scatter Plot)
st.subheader("💵 Tuition vs Enrollment Size")

fig4 = px.scatter(filtered_df, x="Tuition", y="Enrollment Numbers", color="Adjusted Rank", 
                  size="Adjusted Rank", hover_name="College Name", 
                  title="Tuition vs Enrollment Size"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------
# Narrative Insights
st.subheader("📌 Insights & Observations")

st.markdown("""
- Higher tuition does not always correlate with a higher ranking.
- Larger colleges tend to have higher enrollment numbers, but enrollment is spread across various rank tiers.
- The majority of colleges are ranked between 50 and 100.
- Tuition ranges can vary widely depending on rank tier.
- Using rank tiers, we can compare different groups of colleges across various factors like tuition and enrollment.
""")

# ---------------------------
# Data Source & Last Refresh
st.markdown("---")
st.markdown("**Data Source:** https://www.kaggle.com/datasets/dylankarmin/2022-college-rankings-compared-to-tuition-costs")
st.markdown(f"**Last refreshed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
