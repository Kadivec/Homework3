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

        if not filtered_df.empty:
            # --- 1. WORD CLOUD (NEW) ---
            st.subheader(f"Most Frequent Words in {selected_month}")
            # Combine all review text into one string
            text = " ".join(review for review in filtered_df.review)
            
            # Generate word cloud
            wordcloud = WordCloud(background_color="white", width=800, height=400, colormap='magma').generate(text)
            
            # Display using matplotlib
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
            st.divider()

            # --- 2. DATA TABLE ---
            st.subheader(f"Review Details for {selected_month}")
            display_df = filtered_df.copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(display_df[['date', 'review', 'Sentiment', 'Score']], use_container_width=True, hide_index=True)

            st.divider()

            # --- 3. SENTIMENT CHART ---
            st.subheader("Sentiment Distribution")
            summary_df = filtered_df.groupby('Sentiment').agg(
                Count=('Sentiment', 'count'),
                Avg_Confidence=('Score', 'mean')
            ).reset_index()

            chart = alt.Chart(summary_df).mark_bar().encode(
                x=alt.X('Sentiment:N', title="Review Sentiment"),
                y=alt.Y('Count:Q', title="Number of Reviews"),
                color=alt.Color('Sentiment:N', scale=alt.Scale(domain=['POSITIVE', 'NEGATIVE'], range=['#2ecc71', '#e74c3c'])),
                tooltip=['Sentiment', 'Count']
            ).properties(height=400).interactive()

            st.altair_chart(chart, use_container_width=True)
            
        else:
            st.info(f"No reviews found for {selected_month} 2023.")
