# 📚 Student Progress Dashboard

A beautiful, interactive dashboard for tracking student learning progress and practice patterns. Built with Streamlit and MongoDB.

![Dashboard Preview](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)

## ✨ Features

### 📊 Comprehensive Analytics
- **Real-time Metrics**: Track lesson completion, total practices, and student performance
- **Consistency Score**: Measure how regularly students practice across lessons
- **Trend Analysis**: Visualize practice patterns over time with interactive charts
- **Difficulty Heatmap**: Color-coded visualization (🟢 Easy | 🟠 Medium | 🔴 Hard)

### 👤 Student Profiles
- Detailed student information and contact details
- Course duration tracking (time since first lesson)
- Last activity timestamps
- Teacher assignments per lesson

### 📈 Visual Insights
- **Practice Trend Chart**: Track student progress with teacher annotations
- **Progress Ring**: Beautiful circular completion indicator
- **Difficulty Analysis**: Identify which lessons require the most practice
- **Recent Performance**: Monitor last 3 lessons average

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB instance
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/student-dashboard.git
cd student-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
MONGO_USER=your_username
MONGO_PASSWORD=your_password
MONGO_PORT=27017
STUDENTS_DB=students_db
STUDENTS_STATS=student_stats
TOTAL_LESSONS=**
```

4. **Run the dashboard**
```bash
streamlit run main.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 📁 Project Structure
```
student-dashboard/
├── main.py              # Main dashboard application
├── .env                 # Environment variables (create this)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 📦 Dependencies
```txt
streamlit
pandas
pymongo
matplotlib
numpy
python-dotenv
```

## 🎨 Dashboard Sections

### 1. Key Metrics Dashboard
Four prominent cards displaying:
- Current lesson progress
- Total practice count
- Average practices per lesson
- Completion percentage

### 2. Student Profile
- Personal information
- Course engagement metrics
- Quick stats badges (Teacher, Last Practice, Hardest Lesson)

### 3. Practice Analysis (3 Tabs)
- **Trend Analysis**: Line chart with teacher annotations and consistency insights
- **Practice Heatmap**: Color-coded difficulty bar chart
- **Lesson Details**: Complete lesson history table

### 4. All Students Overview
Expandable table showing all students with sortable columns

## 🎯 Understanding the Metrics

### Consistency Score
Measures how evenly practices are distributed across lessons:
- **70-100%**: Excellent - Very regular practice habits
- **50-70%**: Good - Some variation but consistent
- **0-50%**: Needs Improvement - Inconsistent practice patterns

### Color Coding (Heatmap)
- 🟢 **Green (1-2 practices)**: Easy lessons
- 🟠 **Orange (3-4 practices)**: Medium difficulty
- 🔴 **Red (5+ practices)**: Challenging lessons

## 🔧 Configuration

Customize the dashboard by modifying environment variables:
- `TOTAL_LESSONS`: Total number of lessons in the course
- `STUDENTS_DB`: MongoDB database name
- `STUDENTS_STATS`: MongoDB collection name

## 🎨 Design Features

- **Glassmorphism UI**: Modern frosted glass effect cards
- **Gradient Backgrounds**: Beautiful purple/blue gradient theme
- **Dark Mode**: Professional dark theme optimized for extended viewing
- **Responsive Layout**: Adapts to different screen sizes
- **Interactive Charts**: Hover effects and detailed tooltips

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Tips

- Use the sidebar to quickly switch between students
- Click the refresh button to reload data from MongoDB
- Expand "All Students Overview" to compare multiple students
- Look for red bars in the heatmap to identify struggling areas

## 🐛 Troubleshooting

**Hebrew text displaying backwards?**
- The dashboard automatically reverses Hebrew text for proper display
- If issues persist, check matplotlib font settings

