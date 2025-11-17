import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time
import os

st.set_page_config(page_title="US College Ranking", page_icon="🎓", layout="wide")
# Disable fade/transition so charts don't blink between reruns
st.markdown("""
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
""", unsafe_allow_html=True)

#-----------------------------------------------------------------------------------------------
# 1. Bar chart of tuition v college
st.title("Tuition Costs of U.S. Colleges (2022)")
st.caption("Exploring whether higher tuition correlates with higher ranking.")

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "2022USCollegeRankings.csv")
df = pd.read_csv(csv_path)

median_tuition = df["Tuition"].median()
df["Tuition"].fillna(median_tuition, inplace=True)

df["Color"] = df["Adjusted Rank"].apply(lambda x: "gold" if x <= 10 else "blue")

st.write(df.head())

fig_cost = px.scatter(df, x = "Tuition", y = "College Name", color = "Color",
             title = "Tuition Cost / College",
             labels = {"College Name": "College", "Tuition": "Tuition($)"},
             color_discrete_map = {"gold": "gold", "blue": "blue"},
             hover_name = "College Name", hover_data = ["Tuition", "Adjusted Rank"])

st.plotly_chart(fig_cost, use_container_width=True)

statement1 = [
    "The bar chart above helps answering our questions of whether higher tuition correlates with higher rankings."
]

read1 = [
    "The x-axis represents the tuition cost for each college.",
    "The y-axis lists the colleges included in the dataset.",
    "Gold-colored bars represent top 10 colleges, while blue bars represent all others."
]

insight1 = [
    "",
    "",
    ""
]

st.markdown("### Statement:")
for i, f in enumerate(statement1, start=1):
    st.write(f"- {f}")

st.markdown("### How to read this chart:")
for i, f in enumerate(read1, start=1):
    st.write(f"- {f}")

st.markdown("### Observations/Insights:")
for i, f in enumerate(insight1, start=1):
    st.write(f"- {f}")

#---------------------------------------------------------------------------------------
# 2. heatmap of enrollment by rank
st.title("Enrollment Numbers Heatmap by College Rank")
st.caption("Visualizing how enrollment varies across colleges and their ranks.")

# Pivot the data to get ranks on columns and colleges on rows
heatmap_df = df.pivot_table(index="College Name", columns="Adjusted Rank", values="Enrollment Numbers", aggfunc="sum")

# Create heatmap
fig_heatmap = px.imshow(
    heatmap_df,
    labels={"x": "Rank", "y": "College", "color": "Enrollment Numbers"},
    color_continuous_scale="Blues",
    title="Enrollment Heatmap by College and Rank"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# Insights for heatmap
statement2 = [
    "The heatmap above shows the distribution of enrollment across colleges ranked in various tiers."
]

read2 = [
    "The x-axis shows college ranks.",
    "The y-axis lists colleges.",
    "Lighter blue shades represent higher enrollment numbers, and darker shades indicate lower enrollment."
]

insight2 = [
    "",
    "",
    ""
]

st.markdown("### Statement:")
for i, f in enumerate(statement2, start=1):
    st.write(f"- {f}")

st.markdown("### How to read this chart:")
for i, f in enumerate(read2, start=1):
    st.write(f"- {f}")

st.markdown("### Observations/Insights:")
for i, f in enumerate(insight2, start=1):
    st.write(f"- {f}")

#--------------------------------------------------------------------------------------------------------------------
# 3. Donut pie chart for tuition distribution among the top 10
st.title("Tuition Distribution of Top 10 Colleges")
st.caption("Visualizing how tuition amounts compare among the highest-ranked colleges.")

top10 = df.sort_values("Adjusted Rank").head(10)

donut_df = top10[["College Name", "Tuition"]]

fig_rating = px.pie(donut_df, names = "College Name", values = "Tuition",
                    title = "Top 10 Colleges — Tuition Distribution",
                    hole = 0.4)

st.plotly_chart(fig_rating, use_container_width = True)

statement3 = [
    "The donut chart above visualizes how tuition varies among the top 10 colleges."
]

read3 = [
    "Each slice represents the tuition of one of the top 10 colleges.",
    "Larger slices indicate higher tuition costs.",
    "This helps compare elite college affordability."
]

insight3 = [
    "",
    "",
    ""
]

st.markdown("### Statement:")
for i, f in enumerate(statement3, start=1):
    st.write(f"- {f}")

st.markdown("### How to read this chart:")
for i, f in enumerate(read3, start=1):
    st.write(f"- {f}")

st.markdown("### Observations/Insights:")
for i, f in enumerate(insight3, start=1):
    st.write(f"- {f}")

#------------------------------------------------------------------------------------------------------------
# 4. choropleth to show amount of ranked colleges / state
st.title("Aggregate Analysis by Rank Tier")
st.caption("Summarizing tuition and enrollment based on rank tiers.")

# Create rank tiers
def rank_tier(rank):
    if rank <= 10:
        return "Top 10"
    elif rank <= 50:
        return "11-50"
    else:
        return "51+"

df["Rank Tier"] = df["Adjusted Rank"].apply(rank_tier)

# Summarize tuition and enrollment
tier_summary = df.groupby("Rank Tier").agg(
    Avg_Tuition=("Tuition", "mean"),
    Total_Enrollment=("Enrollment Numbers", "sum"),
    Count=("College Name", "count")
).reset_index()

st.write(tier_summary)

# Bar chart: Average Tuition by Rank Tier
fig_tuition_tier = px.bar(tier_summary, x="Rank Tier", y="Avg_Tuition", 
                              title="Average Tuition by Rank Tier",
                              labels={"Avg_Tuition": "Average Tuition ($)"}
)
st.plotly_chart(fig_tuition_tier, use_container_width=True)

# Bar chart: Total Enrollment by Rank Tier
fig_enroll_tier = px.bar(tier_summary, x="Rank Tier", y="Total_Enrollment",
                             title="Total Enrollment by Rank Tier",
                             labels={"Total_Enrollment": "Total Enrollment"}
)
st.plotly_chart(fig_enroll_tier, use_container_width=True)

statement4 = [
    "The choropleth map supports our question about how geography impacts rank and tuition."
]

read4 = [
    "Darker blue states have more ranked colleges.",
    "This can reveal educational hubs and regional inequalities."
]

insight4 = [
    "",
    "",
    ""
]

st.markdown("### Statement:")
for i, f in enumerate(statement4, start=1):
    st.write(f"- {f}")

st.markdown("### How to read this chart:")
for i, f in enumerate(read4, start=1):
    st.write(f"- {f}")

st.markdown("### Observations/Insights:")
for i, f in enumerate(insight4, start=1):
    st.write(f"- {f}")
