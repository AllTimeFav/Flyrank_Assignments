import os
import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com"   
cache_file = "cache/catalogue-page-1.html"

os.makedirs("cache", exist_ok=True)

if os.path.exists(cache_file):
    print("CACHE HIT")
    with open(cache_file, "r", encoding="utf-8") as f:
        html_content = f.read()
else:
    print("FETCH")
    header = {
        "user-agent": "FlyRankInternshipA9/1.0 (+https://github.com/AllTimeFav/Flyrank_Assignments)"
    }
    response = requests.get(url, headers=header, timeout=5)
    
    if response.status_code == 200:
        html_content = response.text
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(html_content)
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        exit(1)

print(f"Response size: {len(html_content)} characters")

soup = BeautifulSoup(html_content, 'html.parser')