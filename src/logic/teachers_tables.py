import streamlit as st
import pandas as pd

from ui.teachers_leadboards import _render_teacher_stats

# TEACHER SELECTOR
def _render_teacher_selector(teacher_data):
    """Dropdown for selecting a teacher."""
    teachers = sorted(teacher_data.keys())
    return st.selectbox("Select a teacher:", teachers)


#TEACHER DETAILS + TABLES
def _render_teacher_details(selected_teacher, teacher_data):
    """Render all information related to the selected teacher."""
    st.markdown(f"## 📚 {selected_teacher}")

    current_students = teacher_data[selected_teacher]["current"]
    past_students = teacher_data[selected_teacher]["past"]

    tab_current, tab_past = st.tabs([
        f"🟢 Current Students ({len(current_students)})",
        f"⚪ Past Students ({len(past_students)})"
    ])

    with tab_current:
        _render_student_table(
            current_students,
            selected_teacher,
            is_current=True
        )

    with tab_past:
        _render_student_table(
            past_students,
            selected_teacher,
            is_current=False
        )

    _render_teacher_stats(selected_teacher, teacher_data)


def _render_student_table(student_list, teacher, is_current):
    """Display a student list inside a tab."""
    if not student_list:
        st.info("No students found.")
        return

    df = pd.DataFrame(student_list).rename(columns={
        "name": "Student Name",
        "current_lesson": "Current Lesson",
        "phone": "Phone Number",
        "last_practice": "Last Practice"
    })

    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    filename = f"{teacher}_{'current' if is_current else 'past'}_students.csv"

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )