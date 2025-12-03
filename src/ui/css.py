import streamlit as st

def inject_css():
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