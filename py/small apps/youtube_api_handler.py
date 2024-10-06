import requests

def get_latest_video(channel_input: str) -> dict:
    import re
    # Extract channel ID from URL if a URL is provided
    channel_url_pattern = r"https?://www\.youtube\.com/[@]([^/?]+)"
    match = re.search(channel_url_pattern, channel_input)
    if match:
        channel_id = match.group(1)
        # Fetch channel ID using YouTube API if URL format is provided
        api_key = 'AIzaSyAA6iUw2M_EMXYDOHhduW7BiToIiXHH7jw'
        base_url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "id",
            "forUsername": channel_id,
            "key": api_key
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch channel information: {e}")
            raise ValueError("Failed to fetch channel information.")
        data = response.json()
        items = data.get("items", [])
        if not items:
            raise ValueError("Channel not found.")
        channel_id = items[0]['id']
    else:
        channel_id = channel_input
    # Proceed with fetching the latest video using the channel ID
    api_key = 'AIzaSyAA6iUw2M_EMXYDOHhduW7BiToIiXHH7jw'
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 1,
        "order": "date",
        "type": "video",
        "key": api_key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch video information: {e}")
        raise ValueError("Failed to fetch video information.")
    data = response.json()
    items = data.get("items", [])
    if not items:
        raise ValueError("No videos found.")
    # Returning all video information as requested
    # print(items[0])
    return items[0]

if __name__ == "__main__":
    video_info = get_latest_video("UCZmzpnJdYlMlZBHJRtXb-Ag")
    video_url = f"https://www.youtube.com/watch?v={video_info['id']['videoId']}"
    print(video_url)
