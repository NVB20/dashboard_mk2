import streamlit as st
from data.mongo import load_students
from teachers_page import render_teachers_page
from students_page import render_students_dashboard

# Your existing constants
TOTAL_LESSONS = 12  # Adjust based on your curriculum

# Load data
df = load_students()

# Sidebar with navigation
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    page = st.radio("Select Page:", ["Student Dashboard", "Teachers Overview"])
    
    st.markdown("---")
    
    # Initialize selected_name variable
    selected_name = None
    
    if page == "Student Dashboard":
        st.markdown("### 🎯 Student Selection")
        if not df.empty:
            student_list = df["name"].tolist()
            selected_name = st.selectbox("Choose a student:", student_list, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Stats")
    st.markdown(f"**Total Students:** {len(df)}")
    st.markdown(f"**Total Lessons:** {TOTAL_LESSONS}")
    
    if not df.empty and "current_lesson" in df.columns:
        avg_completion = df["current_lesson"].astype(int).mean()
        st.markdown(f"**Avg Completion:** {avg_completion:.1f}/{TOTAL_LESSONS}")
    
    st.markdown("---")
    st.markdown("### 🔄 Refresh Data")
    if st.button("🔄 Reload", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Page routing
if page == "Teachers Overview":
    render_teachers_page(df)
if page == "Student Dashboard":
    render_students_dashboard(df, selected_name, TOTAL_LESSONS)