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
# 1. scatter chart of tuition v college
st.title("Tuition Costs of U.S. Colleges (2022)")
st.caption("Exploring whether higher tuition correlates with higher ranking.")

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "2022USCollegeRankings.csv")
df = pd.read_csv(csv_path)

median_tuition = df["Tuition"].median()
df["Tuition"].fillna(median_tuition, inplace=True)

df["Color"] = df["Adjusted Rank"].apply(lambda x: "gold" if x <= 10 else "blue")

college_options = df["College Name"].unique()
selected_college = st.selectbox("Select College", options = ["All Colleges"] + list(college_options), index = 0)

if selected_college != "All Colleges":
    filtered_df = df[df["College Name"] == selected_college]
else:
    filtered_df = df

st.write(df.head())

fig_cost = px.scatter(filtered_df, x = "Tuition", y = "College Name", color = "Color",
             title = "Tuition Cost / College",
             labels = {"College Name": "College", "Tuition": "Tuition($)"},
             color_discrete_map = {"gold": "gold", "blue": "blue"},
             hover_name = "College Name", hover_data = ["Tuition", "Adjusted Rank"])

st.plotly_chart(fig_cost, use_container_width=True)

statement1 = [
    "The scatter chart above helps answering our questions of whether higher tuition correlates with higher rankings."
]

read1 = [
    "The x-axis represents the tuition cost for each college.",
    "The y-axis lists the colleges included in the dataset.",
    "Gold-colored bars represent top 10 colleges, while blue bars represent all others.",
    "Hover mode and college selection is available for this chart."
]

insight1 = [
    "Most colleges in the Top 10 are high in tuition.",
    "Some colleges have high tuition, but low ranking.",
    "University of Florida has a tuition of ~$28K with a ranking of 28."
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

heatmap_df = df.pivot_table(index="College Name", columns="Adjusted Rank", values="Enrollment Numbers", aggfunc="sum")

# Create heatmap focusing on enrollment numbers across rank tiers
fig_heatmap = px.imshow(
    heatmap_df,
    labels={"x": "Rank", "y": "College", "color": "Enrollment Numbers"},
    color_continuous_scale="YlGnBu",
    title="Enrollment Heatmap by Rank"
)

st.plotly_chart(fig_heatmap, use_container_width=True)


# Insights for heatmap
statement2 = [
    "The heatmap above shows the distribution of enrollment across colleges ranked in various tiers."
]

read2 = [
    "The x-axis shows college ranks.",
    "The y-axis lists colleges.",
    "Lighter color shades represent lower enrollment numbers, and darker shades indicate higher enrollment."
    "Zooming in is allowed."
]

insight2 = [
    "University of Central Florida has enrollment of ~62k students, but low ranking.",
    "The top 10 colleges have lower enrollments.",
    "There are higher enrollments the more the rank decreases."
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
st.title("Tuition Distribution of Top 6 Colleges")
st.caption("Visualizing how tuition amounts compare among the highest-ranked colleges.")

top6 = df.sort_values("Adjusted Rank").head(6)

donut_df = top6[["College Name", "Tuition"]]

fig_rating = px.pie(donut_df, names = "College Name", values = "Tuition",
                    title = "Top 6 Colleges — Tuition Distribution",
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
    "The tuition for the top 6 are similar to one another.",
    "The highest tuition is ~63k for Columbia University.",
    "None of the top 6 are less than $55k."
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
# 4. bar to show amount of ranked colleges / state
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
    "The bar charts above summarize college enrollment and tuition based on rank tiers."
]

read4 = [
    "The first chart shows average tuition by rank tier.",
    "The second chart shows total enrollment by rank tier.",
    "Rank tiers are divided into Top 10, 11-50, and 51+."
]

insight4 = [
    "The higher we go in rank, the less enrollments there are.",
    "The total enrollment from ranks 1-50 is ~80k students.",
    "The average tuition cost of rank 11-50 costs almost teh same amount as the top 10."
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
