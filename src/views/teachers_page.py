import streamlit as st

from ui.teachers_css import inject_css
from logic.teachers_metric import categorize_students_by_teacher, _render_summary_metrics
from ui.teachers_leadboards import _render_leaderboard
from logic.teachers_tables import _render_teacher_details, _render_teacher_selector


def render_teachers_page(df):
    """
    Render the full Teachers Overview dashboard.
    Should only run UI logic when this function is called,
    not on module import.
    """

    # Inject global CSS for teachers page
    inject_css()

    st.title("👨‍🏫 Teachers Overview")
    st.markdown("---")

    # Guard: no data available
    if df.empty:
        st.warning("No student data available.")
        return

    # Organize students by teacher
    teacher_data = categorize_students_by_teacher(df)

    # Guard: maybe no teachers field
    if not teacher_data:
        st.info("No teachers found in the system.")
        return

    # --- SUMMARY METRICS ---
    _render_summary_metrics(teacher_data)

    st.markdown("---")

    # --- TEACHER SELECTOR ---
    selected_teacher = _render_teacher_selector(teacher_data)

    st.markdown("---")

    # --- TEACHER DETAILS ---
    if selected_teacher:
        _render_teacher_details(selected_teacher, teacher_data)

    # --- LEADERBOARD ---
    st.markdown("### 🏆 Teacher Leaderboard")
    _render_leaderboard(teacher_data)

