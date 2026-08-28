from urllib3.util import timeout
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

os.makedirs("cache", exist_ok=True)

current_url = "https://books.toscrape.com/"
unique_urls = set()
discovered = 0
catalogue_pages = 0

header = {
    "user-agent": "FlyRankInternshipA9/1.0 (+https://github.com/AllTimeFav/Flyrank_Assignments)"
}

for pages in range(1, 4):
    cache_url = f"cache/catalogue-page-{pages}.html"
    html_content = ""
    
    if os.path.exists(cache_url):
        print("Cahce Hit for ", cache_url)
        with open(cache_url, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        print("Fetch for, ", cache_url)
        try:
            res = requests.get(current_url, headers=header, timeout=5)
            if res.status_code == 200:
                with open(cache_url, "w", encoding="utf-8") as f:
                    f.write(res.text)
                html_content = res.text
               
        except Exception as e:
            print("Exception: ", e)
            continue
        
        time.sleep(0.5)
        
    catalogue_pages += 1
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='product_pod')
    for article in articles:
        link = article.h3.a['href']
        url = urljoin(current_url, link)
        if url not in unique_urls:
            unique_urls.add(url)
            discovered += 1
    
    next_page_button = soup.find('li', class_='next')
    if next_page_button:
        next_page_url = next_page_button.a['href']
        current_url = urljoin(current_url, next_page_url)
    else:
        break   
        

print(f"catalogue_pages={catalogue_pages}, discovered={discovered}, unique_urls={len(unique_urls)}")