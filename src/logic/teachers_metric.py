import streamlit as st

from collections import defaultdict

def get_active_teacher(student):
    """Get the teacher of the most recent lesson for a student."""
    lessons = student.get("lessons", [])
    if not lessons:
        return None
    
    # Find the lesson with the highest lesson number
    max_lesson = max(lessons, key=lambda x: int(x.get("lesson", 0)))
    return max_lesson.get("teacher")


def categorize_students_by_teacher(df):
    """
    Categorize students by teacher into current and past students.
    Current students: those whose most recent lesson is with this teacher
    Past students: those who had lessons with this teacher but moved on
    Also calculates total practice count for each teacher.
    """
    teacher_data = defaultdict(lambda: {"current": [], "past": [], "total_practices": 0})
    
    for _, student in df.iterrows():
        lessons = student.get("lessons", [])
        if not lessons:
            continue
        
        # Get the active teacher (most recent lesson)
        active_teacher = get_active_teacher(student)
        
        # Get all unique teachers this student has worked with
        all_teachers = set(lesson.get("teacher") for lesson in lessons if lesson.get("teacher"))
        
        student_info = {
            "name": student.get("name", "Unknown"),
            "current_lesson": student.get("current_lesson", "N/A"),
            "phone": student.get("phone_number", "N/A"),
            "last_practice": student.get("last_practice_timedate", "N/A")
        }
        
        # Calculate practice counts per teacher
        for lesson in lessons:
            teacher = lesson.get("teacher")
            if teacher:
                practice_count = lesson.get("practice_count", 0)
                try:
                    practice_count = int(practice_count)
                except:
                    practice_count = 0
                teacher_data[teacher]["total_practices"] += practice_count
        
        for teacher in all_teachers:
            if teacher == active_teacher:
                # This is the student's current teacher
                teacher_data[teacher]["current"].append(student_info)
            else:
                # This student worked with this teacher in the past
                teacher_data[teacher]["past"].append(student_info)
    
    return teacher_data

#SUMMARY METRICS
def _render_summary_metrics(teacher_data):
    """Show overall summary metrics for all teachers."""
    total_current = sum(len(data["current"]) for data in teacher_data.values())
    total_past = sum(len(data["past"]) for data in teacher_data.values())
    total_practices = sum(data["total_practices"] for data in teacher_data.values())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Teachers", len(teacher_data))
    col2.metric("Total Current Students", total_current)
    col3.metric("Total Past Students", total_past)
    col4.metric("Total Practices Checked", total_practices)