import streamlit as st
import pandas as pd
import json
import os
import altair as alt

# Page configuration
st.set_page_config(page_title="Web Scraping Dashboard", layout="wide")

# --- HEADER SECTION ---
col_name, col_logo, col_spacer = st.columns([2, 1, 1])
with col_name:
    st.title("Andraž Kadivec | Web Scraping Homework 3")
with col_logo:
    # Official EF Logo
    logo_url = "logo.png"
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

# --- SECTIONS ---
if page == "Products":
    st.header("📦 Product Catalog")
    products = load_json('Products.json')
    if products:
        st.dataframe(pd.DataFrame(products), use_container_width=True, hide_index=True)

elif page == "Testimonials":
    st.header("💬 User Testimonials")
    testimonials = load_json('Testimonials.json')
    if testimonials:
        for t in testimonials:
            with st.container(border=True):
                st.markdown(f"**User:** {t['user']}")
                st.write(f"_{t['testimonial']}_")

elif page == "Reviews":
    st.header("⭐ Customer Reviews & Sentiment Analysis")
    reviews = load_json('Reviews.json')
    
    if reviews:
        df_r = pd.DataFrame(reviews)
        df_r['date'] = pd.to_datetime(df_r['date'])
        
        selected_month = st.select_slider("Select Month in 2023", 
                                        options=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 
                                        value="May")
        
        month_idx = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(selected_month) + 1
        filtered_df = df_r[df_r['date'].dt.month == month_idx].copy()

        if not filtered_df.empty:
            # Displaying columns from your local analysis
            st.dataframe(filtered_df[['date', 'review', 'Sentiment', 'Score']], use_container_width=True, hide_index=True)

            st.divider()
            st.subheader("Sentiment Distribution & Model Confidence")

            # Chart Logic
            summary_df = filtered_df.groupby('Sentiment').agg(
                Count=('Sentiment', 'count'),
                Avg_Confidence=('Score', 'mean')
            ).reset_index()

            summary_df['Avg_Confidence_Label'] = summary_df['Avg_Confidence'].apply(lambda x: f"{x:.2%}")

            chart = alt.Chart(summary_df).mark_bar().encode(
                x=alt.X('Sentiment:N', title="Review Sentiment"),
                y=alt.Y('Count:Q', title="Number of Reviews"),
                color=alt.Color('Sentiment:N', scale=alt.Scale(domain=['POSITIVE', 'NEGATIVE'], range=['#2ecc71', '#e74c3c'])),
                tooltip=['Sentiment', 'Count', 'Avg_Confidence_Label']
            ).properties(height=400).interactive()

            st.altair_chart(chart, use_container_width=True)
