from schema.article import Article
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
total_detail_pages = 0

header = {
    "user-agent": "FlyRankInternshipA9/1.0 (+https://github.com/AllTimeFav/Flyrank_Assignments)"
}

def getDetails(html_content, current_url):
    detail_pages = 0
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='product_pod')
    for article in articles:
        detail_pages += 1
    
        title = article.h3.a['title']
        product_url = urljoin(current_url, article.find('h3').find('a')['href'])
        price_text = article.find('p', class_='price_color').text.strip()
        availability_text = article.find('p', class_='instock availability').text.strip()
        rating = article.find('p', class_="star-rating")['class'][1]
        source_page = current_url
        
        # The description is only on the detail page, not the catalogue page!
        description = '...'
        
        fetched_at = time.time()
        
        price = float(price_text.replace('Â£', ''))

        try:
            a = Article(
                title=title,
                url=product_url,
                price=price_text,
                price_gbp=price,
                availability=availability_text,
                rating=rating,
                source_page=source_page,
                description=description,
                fetched_at=fetched_at
            )

            with open("articles.json", "a", encoding="utf-8") as f:
                f.write(a.model_dump_json() + "\n")
            
            print("Successfully Added")
        except Exception as e:
            with open("errors.json", "a", encoding="utf-8") as f:
                f.write(str(e) + "\n")
            print("Exception: ", e)
    
            
    return detail_pages

for pages in range(1, 4):
    cache_url = f"cache/catalogue-page-{pages}.html"
    html_content = ""
    
    if os.path.exists(cache_url):
        print("Cache Hit for", cache_url)
        with open(cache_url, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        print("Fetch for", cache_url)
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
        
    # Call getDetails outside the if/else so it runs for both cache hits and fresh fetches
    page_details_count = getDetails(html_content, current_url)
    total_detail_pages += page_details_count
        
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
        

print(f"Total Detail Pages overall: {total_detail_pages}")
print(f"catalogue_pages={catalogue_pages}, discovered={discovered}, unique_urls={len(unique_urls)}")