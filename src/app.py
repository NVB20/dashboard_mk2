import streamlit as st
from data.mongo import load_students
from logic.metrics import calculate_student_metrics
from config.settings import TOTAL_LESSONS
from ui.css import inject_css
from ui.layout import render_student_top_metrics, render_student_profile, render_practice_analysis, render_all_students_overview


# Streamlit setup
st.set_page_config(page_title="Student Dashboard", layout="wide")
inject_css()

# Load DB
df = load_students()

if df.empty:
    st.warning("No students found.")
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Student Selection")
    student_list = df["name"].tolist()
    selected_name = st.selectbox("Choose a student:", student_list, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Stats")
    st.markdown(f"**Total Students:** {len(df)}")
    st.markdown(f"**Total Lessons:** {TOTAL_LESSONS}")
    
    avg_completion = df["current_lesson"].astype(int).mean()
    st.markdown(f"**Avg Completion:** {avg_completion:.1f}/{TOTAL_LESSONS}")
    
    st.markdown("---")
    st.markdown("### 🔄 Refresh Data")
    if st.button("🔄 Reload", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Get selected student
student = df[df["name"] == selected_name].iloc[0]
metrics = calculate_student_metrics(student)


# Metrics
metrics = calculate_student_metrics(student)

# Title
st.title("📚 Student Dashboard")

# --- TOP METRICS ---
render_student_top_metrics(student, metrics)

# --- PROFILE SECTION ---
render_student_profile(student)

# --- ANALYSIS SECTION ---
render_practice_analysis(student, metrics)

# --- CHARTS ---
col1, col2 = st.columns(2)

render_all_students_overview(df)