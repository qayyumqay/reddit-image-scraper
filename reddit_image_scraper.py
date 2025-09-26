import requests
import json
import argparse

def scrape_subreddit(subreddit, pages, out_file):
    results = []
    after = None
    headers = {"User-Agent": "Mozilla/5.0 (reddit scraper)"}

    for page in range(1, pages + 1):
        url = f"https://www.reddit.com/r/{subreddit}/.json"
        if after:
            url += f"?after={after}"

        print(f"[{page}/{pages}] Fetching: {url} ...")
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"Error {r.status_code} on page {page}")
            break

        data = r.json()
        posts = data["data"]["children"]

        for post in posts:
            post_data = post["data"]
            if "url" in post_data and (
                post_data["url"].endswith(".jpg") or
                post_data["url"].endswith(".png") or
                post_data["url"].endswith(".jpeg")
            ):
                results.append({
                    "title": post_data.get("title"),
                    "url": post_data.get("url"),
                    "permalink": f"https://reddit.com{post_data.get('permalink')}"
                })

        after = data["data"].get("after")
        if not after:
            break

    print(f"Found {len(results)} posts with images. Writing to {out_file}")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subreddit", required=True, help="Subreddit name")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape")
    parser.add_argument("--out", default="results.json", help="Output JSON file")

    args = parser.parse_args()
    scrape_subreddit(args.subreddit, args.pages, args.out)
