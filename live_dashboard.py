import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firebase (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_service_account.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Streamlit Page Config
st.set_page_config(page_title="Kenya Hospital Dashboard", layout="wide")
st.title("🏥 Kenya Health Facility Live Dashboard")

# Fetch Data from Firebase
@st.cache_data(ttl=3600)
def get_data():
    docs = db.collection("kenya_health_facilities").stream()
    data = [doc.to_dict() for doc in docs]
    return pd.DataFrame(data)

df = get_data()

# Filters
st.sidebar.header("🔍 Filter Facilities")
county = st.sidebar.selectbox("Select County", options=["All"] + sorted(df["County"].dropna().unique().tolist()))
level = st.sidebar.selectbox("Select KePH Level", options=["All"] + sorted(df["KePH Level"].dropna().unique().tolist()))

if county != "All":
    df = df[df["County"] == county]
if level != "All":
    df = df[df["KePH Level"] == level]

# Dashboard Display
st.metric("Total Facilities", len(df))

st.dataframe(df.sort_values(by="County").reset_index(drop=True))
