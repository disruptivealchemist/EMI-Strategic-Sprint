from bs4 import BeautifulSoup
import requests

def crawl_web_mentions(brand_name, num_pages=5):
    mentions = []
    search_url = f"https://www.google.com/search?q={brand_name}&num={num_pages * 10}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for g in soup.find_all('div', class_='BVG0Nb'):
        link = g.find('a')['href']
        mentions.append(link)

    return mentions

def main():
    brand_name = "Emery Industries"
    mentions = crawl_web_mentions(brand_name)
    print("Brand Mentions Found:")
    for mention in mentions:
        print(mention)

if __name__ == "__main__":
    main()