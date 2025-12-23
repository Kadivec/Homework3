import streamlit as st
import pandas as pd
import json
import os
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Web Scraping Dashboard", layout="wide")

# --- HEADER SECTION ---
col_name, col_logo, col_spacer = st.columns([2, 1, 1])
with col_name:
    st.title("Andraž Kadivec | Web Scraping Homework 3")
with col_logo:
    # Points to your logo.png on GitHub
    logo_url = "https://raw.githubusercontent.com/Kadivec/Homework3/main/logo.png"
    st.image(logo_url, width=250)

st.divider()

# --- DATA LOADING ---
script_directory = os.path.dirname(os.path.abspath(__file__))

def load_json(file_name):
    full_path = os.path.join(script_directory, file_name)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose Section:", ["Products", "Testimonials", "Reviews"])

# --- PRODUCTS SECTION ---
if page == "Products":
    st.header("📦 Product Catalog")
    products = load_json('Products.json')
    if products:
        st.dataframe(pd.DataFrame(products), use_container_width=True, hide_index=True)

# --- TESTIMONIALS SECTION ---
elif page == "Testimonials":
    st.header("💬 User Testimonials")
    testimonials = load_json('Testimonials.json')
    if testimonials:
        for t in testimonials:
            with st.container(border=True):
                st.markdown(f"**User:** {t['user']}")
                st.write(f"_{t['testimonial']}_")

# --- REVIEWS SECTION ---
elif page == "Reviews":
    st.header("⭐ Customer Reviews & Sentiment Analysis")
    reviews = load_json('Reviews.json')
    
    if reviews:
        df_r = pd.DataFrame(reviews)
        df_r['date'] = pd.to_datetime(df_r['date'])
        
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        selected_month = st.select_slider("Select Month in 2023", options=months, value="May")
        
        month_idx = months.index(selected_month) + 1
        filtered_df = df_r[df_r['date'].dt.month == month_idx].copy()

        if not filtered_df.empty:
            # 1. Word Cloud
            st.subheader(f"Word Cloud for {selected_month}")
            text = " ".join(review for review in filtered_df.review)
            wordcloud = WordCloud(background_color="white", width=800, height=400, colormap='viridis').generate(text)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
            st.divider()

            # 2. Data Table
            st.subheader("Sentiment Analysis Results")
            st.dataframe(filtered_df[['date', 'review', 'Sentiment', 'Score']], use_container_width=True, hide_index=True)

            # 3. Sentiment Chart
            st.divider()
            summary_df = filtered_df.groupby('Sentiment').size().reset_index(name='Count')
            chart = alt.Chart(summary_df).mark_bar().encode(
                x='Sentiment:N',
                y='Count:Q',
                color=alt.Color('Sentiment:N', scale=alt.Scale(domain=['POSITIVE', 'NEGATIVE'], range=['#2ecc71', '#e74c3c']))
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)
            
        else:
            st.info(f"No reviews found for {selected_month}.")
