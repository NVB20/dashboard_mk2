
import streamlit as st
from pymongo import MongoClient
import pandas as pd
from config.settings import MONGO_USER
from config.settings import MONGO_PASSWORD
from config.settings import MONGO_PORT
from config.settings import MONGO_HOST


# MongoDB Connection
MONGO_URL = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
    "?authSource=admin"
)

client = MongoClient(MONGO_URL)
db = client["students_db"]
collection = db["student_stats"]


# Load Data
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