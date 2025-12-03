import streamlit as st
import pandas as pd

# TEACHER STATISTICS BOXES
def _render_teacher_stats(teacher, teacher_data):
    """Show metrics about a specific teacher."""
    current = teacher_data[teacher]["current"]
    past = teacher_data[teacher]["past"]
    total = len(current) + len(past)
    practices = teacher_data[teacher]["total_practices"]

    st.markdown("---")
    st.markdown("### 📊 Statistics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Students", len(current))
    col2.metric("Past Students", len(past))
    col3.metric("Students - All Time", total)
    col4.metric("Practices Checked", practices)


# LEADERBOARD SECTION
def _render_leaderboard(teacher_data):
    """Display leaderboard of teachers ranked by practices checked."""
    st.markdown("## 🏆 Teachers Leaderboard - Most Practices Checked")

    leaderboard = [
        {
            "Teacher": teacher,
            "Practices Checked": data["total_practices"],
            "Current Students": len(data["current"]),
            "Past Students": len(data["past"]),
            "Total Students": len(data["current"]) + len(data["past"]),
        }
        for teacher, data in teacher_data.items()
    ]

    df = pd.DataFrame(leaderboard)
    df = df.sort_values("Practices Checked", ascending=False)
    df.insert(0, "Rank", range(1, len(df) + 1))

    df["Rank"] = df["Rank"].apply(_add_medal)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Leaderboard CSV",
        data=csv,
        file_name="teachers_leaderboard.csv",
        mime="text/csv"
    )


def _add_medal(rank):
    """Return formatted rank with medal emoji."""
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    return f"{medals.get(rank, '')} {rank}".strip()
