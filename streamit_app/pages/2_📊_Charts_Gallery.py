import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

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

df = pd.read_csv("data/2022USCollegeRankings.csv")

median_tuition = df["Tuition"].median()
df["Tuition"].fillna(median_tuition, inplace=True)

df["Color"] = df["Adjusted Rank"].apply(lambda x: "gold" if x <= 10 else "blue")

st.write(df.head())

fig_cost = px.bar(df, x = "Tuition", y = "College Name", color = "Color",
             title = "Tuition Cost / College",
             labels = {"College Name": "College", "Tuition": "Tuition($)"},
             color_discrete_map = {"gold": "gold", "blue": "blue"},
             hover_name = "College Name", hover_data = ["Tuition", "Adjusted Ranking"])

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
# 2. line chart of enrollment v rank
st.title("Enrollment Trends by College Rank")
st.caption("Visualizing how enrollment size compares across ranking positions.")

rank_enroll_df = df.sort_values("Adjusted Rank").head(20)

fig_sales = px.line(rank_enroll_df, x = "Adjusted Rank", y = "Enrollment Numbers",
                    title = "Enrollment Numbers by College Ranking",
                    labels = {"Adjusted Rank": "Rank", "Enrollment Numbers": "Enrollment"},
                    hover_name = "College Name", color="College Name")

st.plotly_chart(fig_sales, use_container_width = True)

statement2 = [
    "The line chart above helps answering our questions about whether enrollment size affects college ranking."
]

read2 = [
    "The x-axis shows the ranking from 1 to 20.",
    "The y-axis shows the number of enrolled students.",
    "Each line represents one college, allowing comparison across ranks."
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

fig_rating = px.pie(donut_df, names = "College Name", values = "College Name",
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
st.title("Geographical Distribution of Ranked Colleges")
st.caption("A map showing how many top-ranked colleges are found in each U.S. state.")

state_counts = df.groupby("State").size().reset_index(name="College Count")

fig_geo = px.choropleth(state_counts, locations="State", locationmode = "USA-states", color = "College Count",
                        scope = "usa", title = "Number of Ranked Colleges / State",
                        color_continuous_scale="Blues")

st.plotly_chart(fig_geo, use_container_width = True)

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
