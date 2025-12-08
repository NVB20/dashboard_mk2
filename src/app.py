import streamlit as st
from data.mongo import load_students
from views.teachers_page import render_teachers_page
from views.students_page import render_students_dashboard
from config.settings import TOTAL_LESSONS

# Load MongoDB data
df = load_students()


# Sidebar with navigation
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    page = st.radio("Select Page:", ["Student Dashboard", "Teachers Overview"])

    st.markdown("---")

    selected_name = None
    # STUDENT SELECTION + SEARCH
    if page == "Student Dashboard":
        st.markdown("### 🔍 Search Student")

        search_query = st.text_input(
            "Search by name:",
            placeholder="Type to search...",
            label_visibility="collapsed"
        )

        if not df.empty:
            student_list = df["name"].tolist()

            # Case-insensitive filtering
            if search_query:
                filtered_students = [
                    s for s in student_list
                    if search_query.lower() in s.lower()
                ]
            else:
                filtered_students = student_list

            if filtered_students:
                selected_name = st.selectbox(
                    "Choose a student:",
                    filtered_students,
                    label_visibility="collapsed"
                )
            else:
                st.warning("No matching students found.")

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



# Page Routing
if page == "Teachers Overview":
    render_teachers_page(df)

elif page == "Student Dashboard":
    if selected_name:
        render_students_dashboard(df, selected_name, TOTAL_LESSONS)
    else:
        st.info("Please select a student from the sidebar.")
