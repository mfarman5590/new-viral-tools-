import requests

API_KEY = "AIzaSyD_v5XZGyni8aOOd70L3doJhdKmWVSqklQ"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

search_params = {
    "part": "snippet",
    "q": "AI News",
    "type": "video",
    "order": "viewCount",
    "maxResults": 5,
    "key": API_KEY,
}

response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
data = response.json()
print(data)
