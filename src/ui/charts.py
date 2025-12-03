from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def render_progress_ring(current: int, total: int = 18):
    """Modern circular progress indicator"""
    fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    percentage = (current / total) * 100
    
    # Create ring
    size = 0.3
    vals = [current, total - current]
    colors = ['#00d2ff', (1, 1, 1, 0.2)] 
    
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
    """Smooth practice trend with gradient fill and teacher annotations"""
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
    teachers = df["teacher"].values
    
    # Plot line with markers
    ax.plot(x, y, marker='o', linewidth=3, markersize=8, 
            color='#00d2ff', markerfacecolor='white', 
            markeredgecolor='#00d2ff', markeredgewidth=2)
    
    # Fill under curve
    ax.fill_between(x, y, alpha=0.3, color='#00d2ff')
    
    # Add teacher annotations at y=0 on the X-axis
    for i, (lesson_num, practice_cnt, teacher) in enumerate(zip(x, y, teachers)):
        # Shorten teacher name if too long (take first name only)
        teacher_short = teacher.split()[0] if teacher else ""
        
        # Reverse the string to fix Hebrew display (matplotlib reads left-to-right)
        teacher_display = teacher_short[::-1]
        
        # Position at y=0
        ax.text(lesson_num, 0, teacher_display,
               ha='center',
               va='center',
               fontsize=8,
               color='#f093fb',
               weight='bold',
               bbox=dict(boxstyle='round,pad=0.3', 
                        facecolor=(0, 0, 0, 0.6), 
                        edgecolor='none'),
               rotation=0)
    
    # Force integer Y-axis
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Set X-axis to show only lesson numbers (integers)
    ax.set_xticks(x)
    ax.set_xticklabels([int(lesson) for lesson in x])
    
    ax.set_xlabel('Lesson Number', color='white', fontsize=12, weight='bold')
    ax.set_ylabel('Practice Count', color='white', fontsize=12, weight='bold')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.2, color='white', linestyle='--')
    
    return fig