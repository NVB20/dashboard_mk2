import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_HOST = os.getenv("MONGO_HOST")
TOTAL_LESSONS = int(os.getenv("TOTAL_LESSONS"))

print("="*60)
print(MONGO_HOST)
print("="*60)



st.set_page_config(
    page_title="Student Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)