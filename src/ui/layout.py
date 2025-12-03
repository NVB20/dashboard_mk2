import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from config.settings import TOTAL_LESSONS
from ui.charts import render_practice_heatmap, render_progress_ring, render_trend_chart


# ============================
#  TOP METRICS SECTION
# ============================
def render_student_top_metrics(student, metrics):
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        _metric_card("Current Lesson", f"{student['current_lesson']}/{TOTAL_LESSONS}")

    with col2:
        _metric_card("Total Practices", metrics["total_practices"])

    with col3:
        _metric_card("Avg Per Lesson", metrics["avg_practice"])

    with col4:
        _metric_card("Completion Rate", f"{metrics['completion_rate']}%")

    st.markdown("<br>", unsafe_allow_html=True)



# ============================
#  STUDENT PROFILE CARD
# ============================
def render_student_profile(student):
    st.markdown("### 👤 Student Profile")

    col_left, col_right = st.columns([2, 1])

    # ------------------
    # LEFT — student info
    # ------------------
    with col_left:
        duration_text = _calculate_course_duration(student)

        st.markdown(f"""
        <div class="student-card">
            <h2 style='margin-top: 0;'>{student['name']}</h2>
            <p><strong>📱 Phone:</strong> {student['phone_number']}</p>
            <p><strong>⏱️ Time in Course:</strong> {duration_text}</p>
            <p><strong>📅 Last Message:</strong> {student['last_message_timedate']}</p>
            <p><strong>✏️ Last Practice:</strong> {student['last_practice_timedate']}</p>
            <p><strong>💬 Total Messages:</strong> {student['total_messages']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Stats badges under card
        _render_profile_badges(student)

    # ------------------
    # RIGHT — progress ring
    # ------------------
    with col_right:
        st.markdown("<div style='padding: 20px;'>", unsafe_allow_html=True)
        fig = render_progress_ring(int(student["current_lesson"]), TOTAL_LESSONS)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)



# ============================
#  PRACTICE ANALYSIS SECTION
# ============================
def render_practice_analysis(student, metrics):
    st.markdown("### 📊 Practice Analysis")

    lessons = student.get("lessons", [])

    if not lessons:
        st.info("📭 No lesson data available yet")
        return

    tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "🔥 Practice Heatmap", "📋 Lesson Details"])


    # ------------------
    # Trend chart
    # ------------------
    with tab1:
        fig = render_trend_chart(lessons)
        if fig:
            st.pyplot(fig)

        col1, col2 = st.columns(2)

        with col1:
            _info_box(
                "🎯 Consistency Score",
                f"{metrics['consistency_score']}% - "
                f"{'Excellent!' if metrics['consistency_score'] > 70 else 'Good progress' if metrics['consistency_score'] > 50 else 'Room for improvement'}")

        with col2:
            recent = lessons[-3:] if len(lessons) >= 3 else lessons
            recent_avg = np.mean([int(l.get("practice_count", 0)) for l in recent])
            _info_box("📅 Recent Performance", f"{recent_avg:.1f} avg practices (last 3 lessons)")


    # ------------------
    # Heatmap
    # ------------------
    with tab2:
        fig = render_practice_heatmap(lessons)
        if fig:
            st.pyplot(fig)

        practice_counts = [int(l.get("practice_count", 0)) for l in lessons]
        _info_box(
            "📊 Practice Distribution",
            f"Min: {min(practice_counts)} | Max: {max(practice_counts)} | Median: {np.median(practice_counts):.0f}"
        )


    # ------------------
    # Lesson Details Table
    # ------------------
    with tab3:
        df = pd.DataFrame(lessons)
        df = df.sort_values("lesson", ascending=False)
        st.dataframe(df, use_container_width=True, height=400, hide_index=True)



# ============================
#  ALL STUDENTS TABLE
# ============================
def render_all_students_overview(df):
    with st.expander("📋 All Students Overview", expanded=False):
        summary = df.copy()
        summary["current_lesson"] = summary["current_lesson"].astype(int)
        summary = summary.sort_values("current_lesson", ascending=False)

        st.dataframe(
            summary[["name", "phone_number", "current_lesson", "total_messages", "last_practice_timedate"]],
            use_container_width=True,
            hide_index=True
        )



# ============================
#  INTERNAL HELPERS
# ============================
def _metric_card(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def _calculate_course_duration(student):
    lessons = student.get("lessons", [])
    if not lessons:
        return "No data"

    first_practice = lessons[0].get("first_practice")
    if not first_practice or "," not in first_practice:
        return "Unknown"

    try:
        date_part = first_practice.split(",")[1].strip()
        first_date = datetime.strptime(date_part, "%d.%m.%Y")
        days = (datetime.now() - first_date).days

        months = days // 30
        remainder = days % 30

        if months > 0:
            return f"{months} months, {remainder} days"
        return f"{days} days"

    except:
        return "Unknown"



def _render_profile_badges(student):
    lessons = student.get("lessons", [])
    if not lessons:
        return

    # Teacher name
    teacher = lessons[-1].get("teacher", "Unknown")

    # Days since last practice
    last_practice = student.get("last_practice_timedate", "")
    if "," in last_practice:
        try:
            date_part = last_practice.split(",")[1].strip()
            last_date = datetime.strptime(date_part, "%d.%m.%Y")
            days = (datetime.now() - last_date).days
            recency = f"🕐 {days} days ago" if days > 0 else "🕐 Today"
        except:
            recency = "🕐 Unknown"
    else:
        recency = "🕐 Unknown"

    # Hardest lesson
    hardest_idx = max(range(len(lessons)), key=lambda i: int(lessons[i].get("practice_count", 0)))
    hardest = lessons[hardest_idx]
    hardest_text = f"⚠️ Hardest: L{hardest['lesson']} ({hardest['practice_count']} practices)"

    # Render 3 badges
    cols = st.columns(3)
    cols[0].markdown(f"<span class='stats-badge'>👨‍🏫 {teacher}</span>", unsafe_allow_html=True)
    cols[1].markdown(f"<span class='stats-badge'>{recency}</span>", unsafe_allow_html=True)
    cols[2].markdown(f"<span class='stats-badge'>{hardest_text}</span>", unsafe_allow_html=True)



def _info_box(title, main_text, description=None):
    st.markdown(f"""
    <div class="info-box">
        <strong>{title}</strong><br>
        {main_text}
        {"<br><br><small style='opacity:0.8;'>" + description + "</small>" if description else ""}
    </div>
    """, unsafe_allow_html=True)
