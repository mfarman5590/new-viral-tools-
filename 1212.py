import streamlit as st
import pandas as pd
import yt_dlp
import time
import random

# Streamlit App Title
st.title("🚀 YouTube Viral Topics Tool (Using yt-dlp, No API Needed)")

# User Input for Search
keyword = st.text_input("🔍 Enter a Keyword for Search (e.g., AI News, Tech Reviews, Fitness Tips)")

# yt-dlp Function to Fetch Video Details
def get_youtube_search_results(keyword, max_results=20):
    ydl_opts = {
        'quiet': True,
        'default_search': f'ytsearch{max_results}',
        'simulate': True,
        'extract_flat': True,
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
                    "Duration": entry.get("duration", "N/A"),
                    "Thumbnail": entry.get("thumbnail", "N/A"),
                    "URL": entry.get("webpage_url", "N/A")
                })
                
            return results
        except Exception as e:
            return f"❌ Error fetching data: {e}"

# Fetch Data Button
if st.button("🔍 Fetch YouTube Data"):
    if not keyword:
        st.warning("⚠️ Please enter a search keyword!")
    else:
        try:
            st.write("🔍 Searching YouTube for trending videos...")
            search_results = get_youtube_search_results(keyword, max_results=20)

            if search_results and isinstance(search_results, list):
                df = pd.DataFrame(search_results)
                st.success(f"✅ Found {len(search_results)} trending videos!")
                st.dataframe(df)

                # Show video thumbnails & links
                for result in search_results:
                    st.image(result["Thumbnail"], caption=result["Title"], width=200)
                    st.markdown(f"**[{result['Title']}]({result['URL']})**")
                    st.write(f"📺 **Channel:** {result['Channel']} | 👀 **Views:** {result['Views']} | 👍 **Likes:** {result['Likes']}")
                    st.write(f"⏳ **Duration:** {result['Duration']} seconds | 📅 **Uploaded on:** {result['Upload Date']}")
                    st.write("----")

            else:
                st.warning("❌ No results found.")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
