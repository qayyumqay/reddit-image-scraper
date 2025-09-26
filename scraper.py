import requests
import json

# Subreddit nak scrape
subreddit = "wallpapers"
url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=10"

# Reddit API perlu User-Agent
headers = {"User-Agent": "reddit-image-scraper/0.1"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    results = []

    for post in data["data"]["children"]:
        post_data = post["data"]
        title = post_data["title"]
        image_url = post_data.get("url", "")

        if image_url.endswith((".jpg", ".png", ".jpeg")):
            results.append({
                "title": title,
                "image_url": image_url,
                "permalink": "https://reddit.com" + post_data["permalink"]
            })

    # Simpan ke JSON
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("✅ Results saved to results.json")
else:
    print("❌ Failed to fetch data:", response.status_code)
