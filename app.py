import streamlit as st
import pandas as pd
import json
import os
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ... (keep your existing header and data loading code) ...

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
            # --- WORD CLOUD GENERATION ---
            st.divider()
            st.subheader(f"Word Cloud for {selected_month}")
            
            # Combine all reviews into one big string
            text = " ".join(review for review in filtered_df.review)
            
            # Create the word cloud object
            wordcloud = WordCloud(background_color="white", width=800, height=400, colormap='viridis').generate(text)
            
            # Display using matplotlib
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.axis("off")
            st.pyplot(fig)
            ax.imshow(wordcloud, interpolation='bilinear')
            
            st.divider()
            # --- DATA TABLE AND BAR CHART ---
            st.dataframe(filtered_df[['date', 'review', 'Sentiment', 'Score']], use_container_width=True, hide_index=True)
            
            # (Keep your existing Bar Chart code below here)

