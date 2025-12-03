import streamlit as st

def inject_css():
    st.markdown("""
    <style>
        /* Main theme */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 20px rgba(255,255,255,0.3);
            transition: transform 0.3s ease, text-shadow 0.3s ease;
        }
        
        [data-testid="stMetricLabel"] {
            color: rgba(255,255,255,0.8) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: color 0.3s ease, text-shadow 0.3s ease;
        }
        
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 40px rgba(102, 126, 234, 0.2);
            margin: 10px 0;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5), 0 0 60px rgba(102, 126, 234, 0.5), 0 0 80px rgba(118, 75, 162, 0.3);
            background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
            border: 1px solid rgba(255,255,255,0.4);
        }
        
        [data-testid="stMetric"]:hover [data-testid="stMetricValue"] {
            transform: scale(1.05);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 30px rgba(255,255,255,0.6), 0 0 40px rgba(0, 210, 255, 0.4);
        }
        
        [data-testid="stMetric"]:hover [data-testid="stMetricLabel"] {
            color: rgba(255,255,255,1) !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.5);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 20px rgba(255,255,255,0.2);
            transition: all 0.3s ease;
        }
        
        h1:hover, h2:hover, h3:hover {
            text-shadow: 3px 3px 8px rgba(0,0,0,0.5), 0 0 30px rgba(255,255,255,0.5), 0 0 50px rgba(0, 210, 255, 0.4);
            transform: translateX(5px);
        }
        
        /* Dataframe styling */
        [data-testid="stDataFrame"] {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px 0 rgba(31, 38, 135, 0.2);
            transition: all 0.3s ease;
        }
        
        [data-testid="stDataFrame"]:hover {
            background: rgba(255,255,255,0.15);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.4), 0 0 40px rgba(102, 126, 234, 0.3);
        }
        
        .stDataFrame table {
            color: #ffffff;
        }
        
        .stDataFrame table tbody tr {
            transition: all 0.2s ease;
        }
        
        .stDataFrame table tbody tr:hover {
            background: rgba(255,255,255,0.15) !important;
            transform: scale(1.01);
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 5px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.2);
        }
        
        .stTabs [data-baseweb="tab"] {
            color: rgba(255,255,255,0.7);
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(255,255,255,0.15);
            color: rgba(255,255,255,0.9);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px 0 rgba(0, 210, 255, 0.3), 0 0 20px rgba(0, 210, 255, 0.2);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.2) 100%);
            color: #ffffff !important;
            box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.3), 0 0 30px rgba(0, 210, 255, 0.4);
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.3);
            backdrop-filter: blur(10px);
            color: #ffffff;
            box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.2);
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:hover {
            background: rgba(255,255,255,0.25);
            border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.3), 0 0 30px rgba(0, 210, 255, 0.4), 0 0 50px rgba(58, 123, 213, 0.2);
            transform: translateY(-2px);
        }
        
        /* Download button styling */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
            box-shadow: 0 4px 15px 0 rgba(0, 210, 255, 0.4), 0 0 20px rgba(0, 210, 255, 0.2);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(0, 210, 255, 0.6), 0 0 40px rgba(0, 210, 255, 0.5), 0 0 60px rgba(58, 123, 213, 0.3);
        }
        
        /* Info/Warning boxes */
        .stAlert {
            background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.3);
            color: #ffffff;
        }
        
        /* Divider */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.5) 50%, transparent 100%);
            margin: 30px 0;
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
            box-shadow: 0 4px 15px 0 rgba(0, 210, 255, 0.2), 0 0 20px rgba(0, 210, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .info-box:hover {
            box-shadow: 0 6px 20px 0 rgba(0, 210, 255, 0.4), 0 0 40px rgba(0, 210, 255, 0.3);
            transform: translateX(5px);
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
            box-shadow: 0 4px 15px 0 rgba(240, 147, 251, 0.4), 0 0 20px rgba(240, 147, 251, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stats-badge:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 6px 20px 0 rgba(240, 147, 251, 0.6), 0 0 40px rgba(240, 147, 251, 0.5), 0 0 60px rgba(245, 87, 108, 0.4);
            background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
        }
    </style>
    """, unsafe_allow_html=True)