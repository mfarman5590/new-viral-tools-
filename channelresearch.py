import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyCDJ3jsuuQlkzoCdr1J3lUhG5LrZh1AMLM"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# Dropdown menu for niche selection
niche_options = {
    "Relationship Stories": "Breakup, Cheating, Relationship Advice, Love Story",
    "Technology": "AI News, Tech Reviews, Gadgets, Smartphones, Laptops",
    "Health & Fitness": "Workout Tips, Healthy Diet, Mental Health, Weight Loss",
    "Business & Finance": "Stock Market, Crypto, Investing, Business Strategies",
    "Gaming": "New Game Releases, Esports, Game Reviews, Walkthroughs",
    "Education": "Study Tips, Online Courses, Learning Hacks, Exam Preparation"
}

niche = st.selectbox("Select a Niche:", list(niche_options.keys()))

# Pre-filled keywords for selected niche
keywords_input = st.text_area(f"Enter Keywords for {niche} (comma separated):", niche_options[niche])

# Additional Filters
min_views = st.number_input("Minimum Views:", min_value=0, value=1000)
max_views = st.number_input("Maximum Views:", min_value=0, value=1000000)
max_channel_age = st.number_input("Max Channel Age (Months):", min_value=0, value=12)

# Convert input to a list
keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

# Fetch Data Button
if st.button("Fetch Data"):
    if not keywords:
        st.warning("Please enter at least one keyword!")
    else:
        try:
            # Calculate date range
            start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
            all_results = []

            for keyword in keywords:
                st.write(f"Searching for keyword: {keyword}")

                search_params = {
                    "part": "snippet",
                    "q": keyword,
                    "type": "video",
                    "order": "viewCount",
                    "publishedAfter": start_date,
                    "maxResults": 5,
                    "key": API_KEY,
                }

                response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
                data = response.json()

                if "items" not in data or not data["items"]:
                    st.warning(f"No videos found for keyword: {keyword}")
                    continue

                videos = data["items"]
                video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
                channel_ids = [video["snippet"].get("channelId", "") for video in videos]

                if not video_ids or not channel_ids:
                    st.warning(f"Skipping keyword: {keyword} due to missing video/channel data.")
                    continue

                stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
                stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
                stats_data = stats_response.json()

                channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
                channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
                channel_data = channel_response.json()

                stats = stats_data.get("items", [])
                channels = channel_data.get("items", [])

                for video, stat, channel in zip(videos, stats, channels):
                    title = video["snippet"].get("title", "N/A")
                    description = video["snippet"].get("description", "")[:200]
                    video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                    views = int(stat["statistics"].get("viewCount", 0))
                    subs = int(channel["statistics"].get("subscriberCount", 0))

                    if subs < 3000 and min_views <= views <= max_views:
                        all_results.append({
                            "Title": title,
                            "Description": description,
                            "URL": video_url,
                            "Views": views,
                            "Subscribers": subs
                        })

            if all_results:
                df = pd.DataFrame(all_results)
                st.success(f"Found {len(all_results)} results!")
                st.dataframe(df)
                st.download_button(label="Download CSV", data=df.to_csv(index=False), file_name="youtube_results.csv", mime="text/csv")
            else:
                st.warning("No results found within the selected filters.")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
