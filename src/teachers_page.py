import streamlit as st

from ui.teachers_css import inject_css
from logic.teachers_metric import categorize_students_by_teacher, _render_summary_metrics
from ui.teachers_leadboards import _render_leaderboard
from logic.teachers_tables import _render_teacher_details, _render_teacher_selector


#RENDER MAIN TEACHERS PAGE
def render_teachers_page(df):
    """Render the entire Teachers Overview page."""
    inject_css()

    st.title("👨‍🏫 Teachers Overview")
    st.markdown("---")

    if df.empty:
        st.warning("No student data available.")
        return

    teacher_data = categorize_students_by_teacher(df)
    if not teacher_data:
        st.info("No teachers found in the system.")
        return

    _render_summary_metrics(teacher_data)

    st.markdown("---")
    selected_teacher = _render_teacher_selector(teacher_data)

    if selected_teacher:
        _render_teacher_details(selected_teacher, teacher_data)

    st.markdown("---")
    _render_leaderboard(teacher_data)