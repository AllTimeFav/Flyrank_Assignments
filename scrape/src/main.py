from schema.article import Article
import os
import sys
import time
import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

os.makedirs("cache", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Clear old output files
open("books.json", "w", encoding="utf-8").close()
open("errors.json", "w", encoding="utf-8").close()

metrics = {
    "start_time": time.time(),
    "duration": 0.0,
    "pages_fetched": 0,
    "cache_hits": 0,
    "valid_records": 0,
    "invalid_records": 0,
    "failed_pages": 0
}

header = {
    "user-agent": "FlyRankInternshipA9/1.0 (+https://github.com/AllTimeFav/Flyrank_Assignments)"
}

unique_urls = set()
current_url = "https://books.toscrape.com/"

print("--- STAGE 1: DISCOVERY ---")
for page_num in range(1, 4):
    cache_url = f"cache/catalogue-page-{page_num}.html"
    html_content = ""
    
    if os.path.exists(cache_url):
        metrics["cache_hits"] += 1
        print("Cache Hit for", cache_url)
        with open(cache_url, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        print("Fetch for", cache_url)
        try:
            res = requests.get(current_url, headers=header, timeout=5)
            if res.status_code == 200:
                metrics["pages_fetched"] += 1
                with open(cache_url, "w", encoding="utf-8") as f:
                    f.write(res.text)
                html_content = res.text
            else:
                metrics["failed_pages"] += 1
                break
        except Exception as e:
            metrics["failed_pages"] += 1
            break
        
        time.sleep(0.5)
        
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='product_pod')
    for article in articles:
        link = article.h3.a['href']
        url = urljoin(current_url, link)
        unique_urls.add(url)
    
    next_page_button = soup.find('li', class_='next')
    if next_page_button:
        next_page_url = next_page_button.a['href']
        current_url = urljoin(current_url, next_page_url)
    else:
        break

# fake URL
fake_url = "https://books.toscrape.com/catalogue/made-up-book/index.html"
unique_urls.add(fake_url)

print(f"Discovered {len(unique_urls)} URLs (including 1 fake).")


print("--- STAGE 2: EXTRACTION ---")
for i, url in enumerate(list(unique_urls)):
    html_content = ""
    
    attempts = 0
    success = False
    while attempts < 2 and not success:
        attempts += 1
        try:
            res = requests.get(url, headers=header, timeout=5)
            if res.status_code == 200:
                success = True
                metrics["pages_fetched"] += 1
                html_content = res.text
            elif res.status_code in [403, 404]:
                # Do not retry on 403/404
                print(f"Failed {url} with {res.status_code} (no retry)")
                break
            else: # 5xx or other
                print(f"Retrying {url} due to status {res.status_code}")
                time.sleep(1)
        except (requests.Timeout, requests.ConnectionError):
            print(f"Retrying {url} due to timeout/connection error")
            time.sleep(1)
        except Exception as e:
            break
    
    if not success:
        metrics["failed_pages"] += 1
        with open("errors.json", "a", encoding="utf-8") as f:
            f.write(json.dumps({"url": url, "error": "Fetch failed"}) + "\n")
        time.sleep(0.5)
        continue
        
    time.sleep(0.5)

    # Parse detail page
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_main = soup.find('div', class_='product_main')
        title = product_main.h1.text
        price_text = product_main.find('p', class_='price_color').text.strip()
        availability_text = product_main.find('p', class_='instock availability').text.strip()
        rating = product_main.find('p', class_='star-rating')['class'][1]
        
        # Get actual description
        description = "..."
        desc_div = soup.find('div', id='product_description')
        if desc_div and desc_div.find_next_sibling('p'):
            description = desc_div.find_next_sibling('p').text
            
        price = float(re.sub(r'[^\d.]', '', price_text))
        
        a = Article(
            title=title,
            url=url,
            price=price_text,
            price_gbp=price,
            availability=availability_text,
            rating=rating,
            source_page=url,
            description=description,
            fetched_at=time.time()
        )
        
        with open("books.json", "a", encoding="utf-8") as f:
            f.write(a.model_dump_json() + "\n")
        
        print(f"Successfully Added: {title}")
        metrics["valid_records"] += 1
    except Exception as e:
        metrics["invalid_records"] += 1
        with open("errors.json", "a", encoding="utf-8") as f:
            f.write(json.dumps({"url": url, "error": str(e)}) + "\n")
        print(f"Exception parsing {url}: {e}")



metrics["duration"] = time.time() - metrics["start_time"]

with open("output/run-report.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=4)

print("--- RUN COMPLETED ---")
print(f"Metrics written to output/run-report.json:")
print(json.dumps(metrics, indent=4))