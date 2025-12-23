import streamlit as st
import pandas as pd
import json
import os
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. Setup
st.set_page_config(page_title="Dashboard", layout="wide")

# 2. Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Andraž Kadivec | Web Scraping Dashboard")
with col2:
    # This URL points to your logo on GitHub
    logo_url = "https://raw.githubusercontent.com/Kadivec/Homework3/main/logo.png"
    st.image(logo_url, width=200)

st.divider()

# 3. Data Loader
def load_data(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# 4. Sidebar Navigation
page = st.sidebar.radio("Navigate", ["Products", "Testimonials", "Reviews"])

# 5. Page Logic
if page == "Products":
    st.header("📦 Products")
    data = load_data('Products.json')
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)

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
        
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        sel_month = st.select_slider("Select Month", options=months, value="May")
        month_num = months.index(sel_month) + 1
        
        filtered = df[df['date'].dt.month == month_num].copy()
        
        if not filtered.empty:
            # Word Cloud Section
            st.subheader(f"Word Cloud for {sel_month}")
            text = " ".join(review for review in filtered.review)
            wc = WordCloud(background_color="white", width=800, height=400).generate(text)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
            st.divider()
            
            # Sentiment Table
            st.subheader("Sentiment Analysis Results")
            # This table requires 'Sentiment' and 'Score' from your local analysis
            st.dataframe(filtered[['date', 'review', 'Sentiment', 'Score']], use_container_width=True)
        else:
            st.write("No reviews found for this month.")
