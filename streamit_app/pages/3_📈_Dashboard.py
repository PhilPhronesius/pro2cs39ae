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
st.caption("Explore tuition, enrollment, rankings, and geographic distribution of US colleges (2022 dataset).")

# Remove chart fade animation
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

# Fill missing tuition with median
df["Tuition"].fillna(df["Tuition"].median(), inplace=True)

# ---------------------------
# Sidebar Filters
st.sidebar.header("Filters")

state_options = df["State"].sort_values().unique()
selected_states = st.sidebar.multiselect("Select State(s)", options=state_options, default=state_options)

tuition_min, tuition_max = int(df["Tuition"].min()), int(df["Tuition"].max())
selected_tuition = st.sidebar.slider("Tuition Range ($)", tuition_min, tuition_max, (tuition_min, tuition_max))

rank_min, rank_max = int(df["Adjusted Rank"].min()), int(df["Adjusted Rank"].max())
selected_rank = st.sidebar.slider("Rank Range", rank_min, rank_max, (rank_min, rank_max))

# Apply filters
filtered_df = df[
    (df["State"].isin(selected_states)) &
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

fig1 = px.scatter(filtered_df, x="Tuition", y="Adjusted Rank", color="State",
                  hover_name="College Name", size="Enrollment Numbers", 
                  title="Tuition vs Adjusted Rank (Interactive)"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# Visual 2: Enrollment Distribution by State (Bar Chart)
st.subheader("🏫 Enrollment Distribution by State")

state_enrollment = filtered_df.groupby("State")["Enrollment Numbers"].sum().reset_index()

fig2 = px.bar(state_enrollment, x="State", y="Enrollment Numbers",
              title="Total Enrollment by State", labels={"Enrollment Numbers": "Total Enrollment", "State": "State"}, 
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
              hover_data=["State", "Adjusted Rank", "Enrollment Numbers"]
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# Visual 4: Geographical Distribution (Choropleth)
st.subheader("🗺️ Number of Ranked Colleges by State")

state_counts = filtered_df.groupby("State").size().reset_index(name="College Count")

fig4 = px.choropleth(state_counts, locations="State", locationmode="USA-states", 
                     color="College Count", color_continuous_scale="Blues",
                     scope="usa", title="Number of Ranked Colleges per State"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------
# Narrative Insights
st.subheader("📌 Insights & Observations")

st.markdown("""
- Colleges with the highest tuition are not always the top-ranked.
- States with larger populations tend to have more ranked colleges.
- Enrollment varies widely even among top-ranked colleges.
- Filtering by state and rank allows comparison of regional patterns and tuition trends.
- There is a mix of high-tuition, high-enrollment, and mid-ranked colleges across the US.
""")

# ---------------------------
# Data Source & Last Refresh
st.markdown("---")
st.markdown("**Data Source:** https://www.kaggle.com/datasets/dylankarmin/2022-college-rankings-compared-to-tuition-costs")
st.markdown(f"**Last refreshed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
