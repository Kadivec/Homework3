import streamlit as st
import pandas as pd
import json
import os
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Dashboard", layout="wide")

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Andraž Kadivec | Web Scraping Dashboard")
with col2:
    # Uses your logo from GitHub
    logo_url = "https://raw.githubusercontent.com/Kadivec/Homework3/main/logo.png"
    st.image(logo_url, width=200)

st.divider()

# --- DATA LOADING ---
def load_data(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# Sidebar
page = st.sidebar.radio("Navigate", ["Products", "Testimonials", "Reviews"])

# --- PAGES ---
if page == "Products":
    st.header("📦 Products")
    data = load_data('Products.json')
    if data: st.dataframe(pd.DataFrame(data), use_container_width=True)

elif page == "Testimonials":
    st.header("💬 Testimonials")
    data = load_data('Testimonials.json')
    if data:
        for t in data:
            st.info(f"**{t['user']}**: {t['testimonial']}")

elif page == "Reviews":
    st.header("⭐ Reviews & Word Cloud")
    data = load_data('Reviews.json')
    if data:
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Month Filter
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        sel_month = st.select_slider("
