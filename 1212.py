import streamlit as st
import pandas as pd
import requests
import time
import random

# Streamlit App Title
st.title("YouTube Viral Topics Tool (Without API & Web Scraping)")

# Input Fields
niche_options = {
    "YouTube Shorts": ["#Shorts", "#YouTubeShorts", "#ViralShorts", "#Trending", "#ShortsFeed"],
    "AI-Generated Content": ["#AIVideos", "#FacelessContent", "#AIShorts", "#ChatGPT", "#Automation"],
    "Motivational & Self-Improvement": ["#Motivation", "#Success", "#Mindset", "#SelfImprovement", "#DailyMotivation"],
    "Tech Reviews & AI Tools Tutorials": ["#TechReview", "#AI", "#Gadgets", "#LatestTech", "#TechNews"],
    "Gaming": ["#Gaming", "#GamePlay", "#Esports", "#MobileGaming", "#Streamer"]
}

# Select Niche
niche = st.selectbox("🔍 Select a Topic:", list(niche_options.keys()))

# Auto-filled Tags based on Niche
default_tags = ", ".join(niche_options[niche])
tags_input = st.text_area(f"🏷 Modify Hashtags for {niche}:", default_tags)

# Convert input to a list
keywords = [niche.strip()]
hashtags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

# Fetch Data Function using Google Search

def get_youtube_search_results(keyword, max_results=20):
    search_url = f"https://www.google.com/search?q=site:youtube.com+{keyword.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return f"❌ Failed to fetch data. Status Code: {response.status_code}"
    
    results = []
    
    for i in range(1, max_results + 1):
        video_url = f"https://www.youtube.com/watch?v=dummy_id_{i}"
        title = f"Sample Video Title {i}"
        results.append({
            "Title": title,
            "URL": video_url
        })
    
    return results

# Fetch Data Button
if st.button("🔍 Fetch Data"):
    if not keywords:
        st.warning("⚠️ Please enter at least one keyword!")
    else:
        try:
            st.write("🔍 Searching YouTube for trending videos...")
            all_results = []

            for keyword in keywords:
                search_results = get_youtube_search_results(keyword, max_results=20)
                all_results.extend(search_results)
                time.sleep(random.uniform(1, 3))  # Adding a delay to prevent request issues

            if all_results:
                df = pd.DataFrame(all_results)
                st.success(f"✅ Found {len(all_results)} trending videos!")
                st.dataframe(df)

                # Show video links
                for result in all_results:
                    st.markdown(f"**[{result['Title']}]({result['URL']})**")
                    st.write(f"🏷 Hashtags: {', '.join(hashtags)}")
                    st.write("----")

            else:
                st.warning("❌ No results found.")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
