import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Load environment variables
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_PORT = os.getenv("MONGO_PORT")
TOTAL_LESSONS = int(os.getenv("TOTAL_LESSONS"))

# -------------------------
# MongoDB Connection
# -------------------------
MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:{MONGO_PORT}/?authSource=admin"

client = MongoClient(MONGO_URL)
db = client["students_db"]
collection = db["student_stats"]

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Student Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
    /* Main theme */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 10px 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Student card */
    .student-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 20px 0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Progress bar custom */
    .progress-container {
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        padding: 5px;
        margin: 10px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        height: 30px;
        border-radius: 8px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(0, 210, 255, 0.2) 0%, rgba(58, 123, 213, 0.2) 100%);
        border-left: 4px solid #00d2ff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
    }
    
    /* Stats badge */
    .stats-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 4px 15px 0 rgba(240, 147, 251, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Load Data
# -------------------------
@st.cache_data(ttl=60)
def load_students():
    docs = list(collection.find())

    if not docs:
        return pd.DataFrame()

    for d in docs:
        for lesson in d.get("lessons", []):
            try:
                lesson["practice_count"] = int(lesson["practice_count"])
            except:
                pass

    df = pd.DataFrame(docs)

    if "_id" in df.columns:
        df = df.drop(columns=["_id"])

    return df

# -------------------------
# Metrics Calculations
# -------------------------
def calculate_student_metrics(student):
    lessons = student.get("lessons", [])
    
    if not lessons:
        return {
            "total_practices": 0,
            "avg_practice": 0,
            "completion_rate": 0,
            "consistency_score": 0
        }
    
    total_practices = sum(int(l.get("practice_count", 0)) for l in lessons)
    avg_practice = total_practices / len(lessons) if lessons else 0
    completion_rate = (int(student.get("current_lesson", 0)) / TOTAL_LESSONS) * 100
    
    # Consistency score: measures regularity of practice habits
    # Higher score = more consistent practice across lessons
    # Score ranges: 70-100% (Excellent), 50-70% (Good), 0-50% (Needs improvement)
    practice_counts = [int(l.get("practice_count", 0)) for l in lessons]
    if len(practice_counts) > 1 and np.mean(practice_counts) > 0:
        std_dev = np.std(practice_counts)
        mean_val = np.mean(practice_counts)
        # Calculate coefficient of variation and invert it
        consistency_score = (1 - (std_dev / mean_val)) * 100
        consistency_score = max(0, min(100, consistency_score))  # Clamp between 0-100
    else:
        consistency_score = 100 if practice_counts and practice_counts[0] > 0 else 0
    
    return {
        "total_practices": total_practices,
        "avg_practice": round(avg_practice, 1),
        "completion_rate": round(completion_rate, 1),
        "consistency_score": round(consistency_score, 1)
    }

# -------------------------
# Visualizations
# -------------------------
def render_progress_ring(current: int, total: int = 18):
    """Modern circular progress indicator"""
    fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    percentage = (current / total) * 100
    
    # Create ring
    size = 0.3
    vals = [current, total - current]
    colors = ['#00d2ff', (1, 1, 1, 0.2)]  # Using tuple format for RGBA
    
    wedges, texts = ax.pie(vals, colors=colors, startangle=90, counterclock=False,
                            wedgeprops=dict(width=size, edgecolor='none'))
    
    # Center text
    ax.text(0, 0, f'{current}\nof {total}', ha='center', va='center',
            fontsize=20, weight='bold', color='white')
    
    ax.axis('equal')
    return fig

def render_practice_heatmap(lessons):
    """Practice intensity heatmap"""
    if not lessons:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 2), dpi=120)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    lesson_nums = [int(l.get("lesson", 0)) for l in lessons]
    practice_counts = [int(l.get("practice_count", 0)) for l in lessons]
    
    colors = plt.cm.plasma(np.array(practice_counts) / max(practice_counts) if practice_counts else [1])
    
    ax.bar(lesson_nums, practice_counts, color=colors, edgecolor='white', linewidth=1)
    ax.set_xlabel('Lesson Number', color='white', fontsize=12)
    ax.set_ylabel('Practices', color='white', fontsize=12)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, color='white')
    
    return fig

def render_trend_chart(lessons):
    """Smooth practice trend with gradient fill"""
    if not lessons:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 4), dpi=120)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    df = pd.DataFrame(lessons)
    df["lesson"] = pd.to_numeric(df["lesson"], errors="coerce")
    df["practice_count"] = pd.to_numeric(df["practice_count"], errors="coerce")
    df = df.sort_values("lesson")
    
    x = df["lesson"].values
    y = df["practice_count"].values
    
    # Plot line with markers
    ax.plot(x, y, marker='o', linewidth=3, markersize=8, 
            color='#00d2ff', markerfacecolor='white', 
            markeredgecolor='#00d2ff', markeredgewidth=2)
    
    # Fill under curve
    ax.fill_between(x, y, alpha=0.3, color='#00d2ff')
    
    # Force integer Y-axis
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    ax.set_xlabel('Lesson Number', color='white', fontsize=12, weight='bold')
    ax.set_ylabel('Practice Count', color='white', fontsize=12, weight='bold')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.2, color='white', linestyle='--')
    
    return fig

# -------------------------
# Dashboard Layout
# -------------------------
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>📚 Student Progress Dashboard</h1>", unsafe_allow_html=True)

df = load_students()

if df.empty:
    st.warning("⚠️ No students found in MongoDB")
    st.stop()

# -------------------------
# Sidebar - Student Selection & Filters
# -------------------------
with st.sidebar:
    st.markdown("### 🎯 Student Selection")
    student_list = df["name"].tolist()
    selected_name = st.selectbox("Choose a student:", student_list, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Stats")
    st.markdown(f"**Total Students:** {len(df)}")
    st.markdown(f"**Total Lessons:** {TOTAL_LESSONS}")
    
    avg_completion = df["current_lesson"].astype(int).mean()
    st.markdown(f"**Avg Completion:** {avg_completion:.1f}/{TOTAL_LESSONS}")
    
    st.markdown("---")
    st.markdown("### 🔄 Refresh Data")
    if st.button("🔄 Reload", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Get selected student
student = df[df["name"] == selected_name].iloc[0]
metrics = calculate_student_metrics(student)

# -------------------------
# Top Metrics Row
# -------------------------
st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Current Lesson</div>
        <div class="metric-value">{student['current_lesson']}/{TOTAL_LESSONS}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Practices</div>
        <div class="metric-value">{metrics['total_practices']}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Avg Per Lesson</div>
        <div class="metric-value">{metrics['avg_practice']}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Completion Rate</div>
        <div class="metric-value">{metrics['completion_rate']}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# Student Profile Section
# -------------------------
st.markdown("### 👤 Student Profile")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown(f"""
    <div class="student-card">
        <h2 style='margin-top: 0;'>{student['name']}</h2>
        <p><strong>📱 Phone:</strong> {student['phone_number']}</p>
        <p><strong>📅 Last Message:</strong> {student['last_message_timedate']}</p>
        <p><strong>✏️ Last Practice:</strong> {student['last_practice_timedate']}</p>
        <p><strong>💬 Total Messages:</strong> {student['total_messages']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats badges below the card - unique insights not shown above
    lessons = student.get("lessons", [])
    
    # Calculate unique metrics
    if lessons:
        last_lesson = lessons[-1]
        teacher_name = last_lesson.get('teacher', 'Unknown')
        
        # Days since last practice
        try:
            last_practice_str = student.get('last_practice_timedate', '')
            # Parse format "13:05, 02.12.2025"
            if last_practice_str and ',' in last_practice_str:
                date_part = last_practice_str.split(',')[1].strip()
                last_practice_date = datetime.strptime(date_part, '%d.%m.%Y')
                days_since = (datetime.now() - last_practice_date).days
                recency_text = f"🕐 {days_since} days ago" if days_since > 0 else "🕐 Today"
            else:
                recency_text = "🕐 Unknown"
        except:
            recency_text = "🕐 Unknown"
        
        # Most challenging lesson (most practices needed)
        hardest_lesson_idx = max(range(len(lessons)), key=lambda i: int(lessons[i].get('practice_count', 0)))
        hardest_lesson = lessons[hardest_lesson_idx]
        hardest_text = f"⚠️ Hardest: L{hardest_lesson.get('lesson')} ({hardest_lesson.get('practice_count')} practices)"
    else:
        teacher_name = "Unknown"
        recency_text = "🕐 No data"
        hardest_text = "⚠️ No data"
    
    badge_cols = st.columns(3)
    with badge_cols[0]:
        st.markdown(f"<span class='stats-badge'>👨‍🏫 {teacher_name}</span>", unsafe_allow_html=True)
    with badge_cols[1]:
        st.markdown(f"<span class='stats-badge'>{recency_text}</span>", unsafe_allow_html=True)
    with badge_cols[2]:
        st.markdown(f"<span class='stats-badge'>{hardest_text}</span>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div style='padding: 20px;'>", unsafe_allow_html=True)
    fig = render_progress_ring(int(student['current_lesson']), TOTAL_LESSONS)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Practice Analysis
# -------------------------
st.markdown("### 📊 Practice Analysis")

lessons = student.get("lessons", [])

if lessons:
    tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "🔥 Practice Heatmap", "📋 Lesson Details"])
    
    with tab1:
        fig = render_trend_chart(lessons)
        if fig:
            st.pyplot(fig)
        
        # Additional insights
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <strong>🎯 Consistency Score</strong><br>
                {metrics['consistency_score']}% - {'Excellent!' if metrics['consistency_score'] > 70 else 'Good progress' if metrics['consistency_score'] > 50 else 'Room for improvement'}
                <br><br>
                <small style='opacity: 0.8;'>Measures how evenly distributed practice sessions are across lessons. Higher scores indicate more regular practice habits.</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            recent_lessons = lessons[-3:] if len(lessons) >= 3 else lessons
            recent_avg = sum(int(l.get("practice_count", 0)) for l in recent_lessons) / len(recent_lessons)
            st.markdown(f"""
            <div class="info-box">
                <strong>📅 Recent Performance</strong><br>
                {recent_avg:.1f} avg practices (last 3 lessons)
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        fig = render_practice_heatmap(lessons)
        if fig:
            st.pyplot(fig)
        
        # Practice distribution
        practice_counts = [int(l.get("practice_count", 0)) for l in lessons]
        st.markdown(f"""
        <div class="info-box">
            <strong>📊 Practice Distribution</strong><br>
            Min: {min(practice_counts)} | Max: {max(practice_counts)} | 
            Median: {np.median(practice_counts):.0f}
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        lesson_df = pd.DataFrame(lessons)
        lesson_df = lesson_df.sort_values("lesson", ascending=False)
        
        # Style the dataframe
        st.dataframe(
            lesson_df,
            use_container_width=True,
            height=400,
            hide_index=True
        )

else:
    st.info("📭 No lesson data available yet")

# -------------------------
# All Students Overview
# -------------------------
with st.expander("📋 All Students Overview", expanded=False):
    # Calculate summary stats
    summary_df = df.copy()
    summary_df["current_lesson"] = summary_df["current_lesson"].astype(int)
    summary_df = summary_df.sort_values("current_lesson", ascending=False)
    
    st.dataframe(
        summary_df[["name", "phone_number", "current_lesson", "total_messages", "last_practice_timedate"]],
        use_container_width=True,
        hide_index=True
    )