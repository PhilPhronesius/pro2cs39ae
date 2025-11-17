# pages/4_🧭_Future_Work.py
import streamlit as st

st.set_page_config(page_title="Future Work", page_icon="🧭", layout="wide")

st.title("🧭 Future Work & Reflection")
st.caption("Planned improvements and lessons learned from the US College Dashboard project.")

# ---------------------------
# Next Steps
st.subheader("Next Steps / Planned Enhancements")

st.markdown("""
1. **Enhanced Interactivity:** Add multi-select filters for majors, college type (public/private), and region for more granular insights.
2. **Accessibility Audit:** Implement a full accessibility review including color-blind palettes, keyboard navigation, and screen reader support.
3. **Advanced KPIs & Visuals:** Include normalized metrics like tuition per student outcome, interactive heatmaps, or comparative scatterplots.
""")

# ---------------------------
# Reflection
st.subheader("Reflection")

st.markdown("""
- The Lab 4.3 prototype was mostly static and focused on individual charts, whereas the final build is **interactive** and filter-driven.
- Linked filters allow users to explore **multiple KPIs simultaneously**, improving usability and insight generation.
- Added narrative and accessibility considerations to make visualizations **more interpretable and inclusive**.
- The final dashboard integrates **real-world US college data (>100 rows)** instead of mock data, enabling reproducible insights.
""")
