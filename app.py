import streamlit as st
import pandas as pd
import json
import os
import altair as alt

# Page configuration
st.set_page_config(page_title="Web Scraping Dashboard", layout="wide")

# --- HEADER SECTION ---
col_name, col_logo, col_spacer = st.columns([1, 1, 1])
with col_name:
    st.markdown("### Andraž Kadivec | Web Scraping Homework 3")
with col_logo:
    # EF Ljubljana Logo
    logo_url = "https://www.acs-giz.si/wp-content/uploads/2025/07/EKONOMSKA-F_logoENG-HOR-CMYK_color-scaled.png"
    st.image(logo_url, width=200)

st.divider()

# --- AUTO-PATH LOGIC ---
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

# --- REVIEWS SECTION (UPDATED FOR PRE-ANALYZED DATA) ---
elif page == "Reviews":
    st.header("⭐ Customer Reviews & Sentiment Analysis")
    reviews = load_json('Reviews.json')
    
    if reviews:
        df_r = pd.DataFrame(reviews)
        df_r['date'] = pd.to_datetime(df_r['date'])
        
        # Month Selector
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        selected_month = st.select_slider("Select Month in 2023", options=months, value="May")
        
        month_idx = months.index(selected_month) + 1
        filtered_df = df_r[df_r['date'].dt.month == month_idx].copy()

        st.subheader(f"Reviews for {selected_month} 2023")
        
        if not filtered_df.empty:
            # Display the data table
            display_df = filtered_df.copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            
            # Show the Sentiment and Score columns from your JSON
            st.dataframe(
                display_df[['date', 'review', 'Sentiment', 'Score']],
                use_container_width=True,
                hide_index=True
            )

            st.divider()
            st.subheader("Sentiment Distribution")

            # Chart Logic using your pre-calculated 'Sentiment' and 'Score'
            summary_df = filtered_df.groupby('Sentiment').agg(
                Count=('Sentiment', 'count'),
                Avg_Confidence=('Score', 'mean')
            ).reset_index()

            summary_df['Avg_Confidence_Label'] = summary_df['Avg_Confidence'].apply(lambda x: f"{x:.2%}")

            chart = alt.Chart(summary_df).mark_bar().encode(
                x=alt.X('Sentiment:N', title="Review Sentiment"),
                y=alt.Y('Count:Q', title="Number of Reviews"),
                color=alt.Color('Sentiment:N', scale=alt.Scale(domain=['POSITIVE', 'NEGATIVE'], range=['#2ecc71', '#e74c3c'])),
                tooltip=[
                    alt.Tooltip('Sentiment:N', title='Sentiment'),
                    alt.Tooltip('Count:Q', title='Review Count'),
                    alt.Tooltip('Avg_Confidence_Label:N', title='Avg. Model Confidence')
                ]
            ).properties(height=400).interactive()

            st.altair_chart(chart, use_container_width=True)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Reviews", len(filtered_df))
            col2.metric("Positive", len(filtered_df[filtered_df['Sentiment'] == 'POSITIVE']))
            col3.metric("Negative", len(filtered_df[filtered_df['Sentiment'] == 'NEGATIVE']))
        else:
            st.info(f"No reviews found for {selected_month} 2023.")
    else:
        st.error("Missing: Reviews.json")