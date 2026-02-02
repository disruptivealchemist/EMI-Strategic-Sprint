from bs4 import BeautifulSoup
import requests

def scrape_social_media(platform_url, brand_name):
    response = requests.get(platform_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {platform_url}")

    soup = BeautifulSoup(response.text, 'html.parser')
    mentions = []

    # Example logic for scraping mentions
    for post in soup.find_all('div', class_='post'):
        if brand_name.lower() in post.text.lower():
            mentions.append(post.text)

    return mentions

def collect_social_mentions(brand_name):
    platforms = {
        "Twitter": "https://twitter.com/search?q=" + brand_name,
        "Facebook": "https://www.facebook.com/search/top?q=" + brand_name,
        "Instagram": "https://www.instagram.com/explore/tags/" + brand_name.replace(" ", "") + "/"
    }

    all_mentions = {}
    for platform, url in platforms.items():
        all_mentions[platform] = scrape_social_media(url, brand_name)

    return all_mentions