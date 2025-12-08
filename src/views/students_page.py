import streamlit as st
from logic.metrics import calculate_student_metrics
from ui.css import inject_css
from ui.layout import (
    render_student_top_metrics,
    render_student_profile,
    render_practice_analysis,
    render_all_students_overview
)

def render_students_dashboard(df, selected_name, total_lessons):
    """
    Renders the student dashboard page.
    Must contain ONLY UI inside this function.
    """

    # Safety check — avoids crashes if no student selected
    if not selected_name:
        st.info("Please select a student from the sidebar.")
        return

    # Inject global CSS
    inject_css()

    # Pull student record
    student_row = df[df["name"] == selected_name]

    if student_row.empty:
        st.error("Student not found in DB.")
        return

    student = student_row.iloc[0]

    # Compute metrics once
    metrics = calculate_student_metrics(student)

    # ----------------------------------------------------
    # PAGE CONTENT
    # ----------------------------------------------------

    st.title("📚 Student Dashboard")

    # --- TOP METRICS ---
    render_student_top_metrics(student, metrics)

    # --- PROFILE SECTION ---
    render_student_profile(student)

    # --- ANALYSIS SECTION ---
    render_practice_analysis(student, metrics)

    # --- CHARTS / ALL STUDENTS OVERVIEW ---
    st.markdown("### 📊 Overall Student Analytics")
    render_all_students_overview(df)
