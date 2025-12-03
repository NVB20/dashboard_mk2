import numpy as np
from config.settings import TOTAL_LESSONS

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