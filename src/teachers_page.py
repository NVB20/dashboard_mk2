import streamlit as st
import pandas as pd
from collections import defaultdict
from ui.teachers_css import inject_css

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


def render_teachers_page(df):
    """Render the teachers overview page."""
    inject_css()
    
    st.title("👨‍🏫 Teachers Overview")
    st.markdown("---")
    
    if df.empty:
        st.warning("No student data available.")
        return
    
    # Get teacher data
    teacher_data = categorize_students_by_teacher(df)
    
    if not teacher_data:
        st.info("No teachers found in the system.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Teachers", len(teacher_data))
    with col2:
        total_current = sum(len(data["current"]) for data in teacher_data.values())
        st.metric("Total Current Students", total_current)
    with col3:
        total_past = sum(len(data["past"]) for data in teacher_data.values())
        st.metric("Total Past Students", total_past)
    with col4:
        total_practices = sum(data["total_practices"] for data in teacher_data.values())
        st.metric("Total Practices Checked", total_practices)
    
    st.markdown("---")
    
    # Teacher selector
    teachers = sorted(teacher_data.keys())
    selected_teacher = st.selectbox("Select a teacher:", teachers)
    
    if selected_teacher:
        st.markdown(f"## 📚 {selected_teacher}")
        
        current_students = teacher_data[selected_teacher]["current"]
        past_students = teacher_data[selected_teacher]["past"]
        
        # Tabs for current and past students
        tab1, tab2 = st.tabs([
            f"🟢 Current Students ({len(current_students)})",
            f"⚪ Past Students ({len(past_students)})"
        ])
        
        with tab1:
            if current_students:
                st.markdown("### Active Students")
                
                # Convert to DataFrame for better display
                current_df = pd.DataFrame(current_students)
                current_df = current_df.rename(columns={
                    "name": "Student Name",
                    "current_lesson": "Current Lesson",
                    "phone": "Phone Number",
                    "last_practice": "Last Practice"
                })
                
                st.dataframe(
                    current_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download button
                csv = current_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Current Students CSV",
                    data=csv,
                    file_name=f"{selected_teacher}_current_students.csv",
                    mime="text/csv"
                )
            else:
                st.info("No current students for this teacher.")
        
        with tab2:
            if past_students:
                st.markdown("### Past Students")
                
                # Convert to DataFrame for better display
                past_df = pd.DataFrame(past_students)
                past_df = past_df.rename(columns={
                    "name": "Student Name",
                    "current_lesson": "Current Lesson",
                    "phone": "Phone Number",
                    "last_practice": "Last Practice"
                })
                
                st.dataframe(
                    past_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download button
                csv = past_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Past Students CSV",
                    data=csv,
                    file_name=f"{selected_teacher}_past_students.csv",
                    mime="text/csv"
                )
            else:
                st.info("No past students for this teacher.")
        
        # Statistics section
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Students", len(current_students))
        with col2:
            st.metric("Past Students", len(past_students))
        with col3:
            total = len(current_students) + len(past_students)
            st.metric("Students - All Time", total)
        with col4:
            practices_checked = teacher_data[selected_teacher]["total_practices"]
            st.metric("Practices Checked", practices_checked)
    
    # Leaderboard section
    st.markdown("---")
    st.markdown("## 🏆 Teachers Leaderboard - Most Practices Checked")
    
    # Create leaderboard data
    leaderboard_data = []
    for teacher, data in teacher_data.items():
        leaderboard_data.append({
            "Teacher": teacher,
            "Practices Checked": data["total_practices"],
            "Current Students": len(data["current"]),
            "Past Students": len(data["past"]),
            "Total Students": len(data["current"]) + len(data["past"])
        })
    
    # Sort by practices checked (descending)
    leaderboard_df = pd.DataFrame(leaderboard_data)
    leaderboard_df = leaderboard_df.sort_values("Practices Checked", ascending=False)
    leaderboard_df.insert(0, "Rank", range(1, len(leaderboard_df) + 1))
    
    # Add medal emojis for top 3
    def add_medal(rank):
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "🥉"
        else:
            return ""
    
    leaderboard_df["Medal"] = leaderboard_df["Rank"].apply(add_medal)
    leaderboard_df["Rank"] = leaderboard_df.apply(lambda row: f"{row['Medal']} {row['Rank']}" if row['Medal'] else str(row['Rank']), axis=1)
    leaderboard_df = leaderboard_df.drop(columns=["Medal"])
    
    # Display leaderboard
    st.dataframe(
        leaderboard_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.TextColumn("Rank", width="small"),
            "Teacher": st.column_config.TextColumn("Teacher", width="medium"),
            "Practices Checked": st.column_config.NumberColumn(
                "Practices Checked",
                format="%d ✅",
                width="medium"
            ),
            "Current Students": st.column_config.NumberColumn("Current", width="small"),
            "Past Students": st.column_config.NumberColumn("Past", width="small"),
            "Total Students": st.column_config.NumberColumn("Total", width="small")
        }
    )
    
    # Download leaderboard
    csv = leaderboard_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Leaderboard CSV",
        data=csv,
        file_name="teachers_leaderboard.csv",
        mime="text/csv"
    )