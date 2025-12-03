import streamlit as st
from logic.metrics import calculate_student_metrics
from ui.css import inject_css
from ui.layout import render_student_top_metrics, render_student_profile, render_practice_analysis, render_all_students_overview



def render_students_dashboard(df, selected_name, total_lessons):
    inject_css()
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