import streamlit as st
import pandas as pd
import yt_dlp
import time
import random

# Streamlit App Title
st.title("YouTube Viral Topics Tool (Without API)")

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

# yt-dlp Function
def get_youtube_search_results(keyword, max_results=5):
    """Fetch multiple trending videos for a given keyword using yt_dlp"""
    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'noplaylist': True,
        'default_search': f'ytsearch{max_results}',  # Search mode
    }

    results = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(keyword, download=False)
            
            for entry in info.get('entries', []):
                results.append({
                    "Title": entry.get("title", "N/A"),
                    "Channel": entry.get("uploader", "N/A"),
                    "Views": entry.get("view_count", "N/A"),
                    "Likes": entry.get("like_count", "N/A"),
                    "Upload Date": entry.get("upload_date", "N/A"),
                    "Description": entry.get("description", "N/A")[:500],
                    "Duration": entry.get("duration", "N/A"),
                    "Thumbnail": entry.get("thumbnail", "N/A"),
                    "URL": entry.get("webpage_url", "N/A")
                })
                
            return results
        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")
            return []

# Fetch Data Button
if st.button("🔍 Fetch Data"):
    if not keywords:
        st.warning("⚠️ Please enter at least one keyword!")
    else:
        try:
            st.write("🔍 Searching YouTube for trending videos...")
            all_results = []

            for keyword in keywords:
                search_results = get_youtube_search_results(keyword, max_results=5)
                all_results.extend(search_results)
                
                # Random delay between searches to avoid detection
                time.sleep(random.uniform(2, 5))

            if all_results:
                df = pd.DataFrame(all_results)
                st.success(f"✅ Found {len(all_results)} trending videos!")
                st.dataframe(df)

                # Show thumbnails
                for result in all_results:
                    st.image(result["Thumbnail"], caption=result["Title"], width=200)
                    st.markdown(f"**[{result['Title']}]({result['URL']})**")
                    st.write(f"📺 Channel: {result['Channel']} | 👀 Views: {result['Views']}")
                    st.write(f"🏷 Hashtags: {', '.join(hashtags)}")
                    st.write("----")

            else:
                st.warning("❌ No results found.")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
