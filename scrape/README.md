# Web Scraping Assignment

## Target classification

- **Which site:** [books.toscrape.com](https://books.toscrape.com/)
- **Why:** The site explicitly states it is a "fictional bookstore that desperately wants to be scraped," serving as a sandbox for beginners to learn and practice web scraping.
- **How much:** The first 3 catalogue pages and their 60 detail pages.
- **What data you collect:** Book title, URL, price, price_gbp, rating, availability status, description, source page, and fetched_at timestamp.
- **Why that is appropriate here:** Because the site is designed and designated specifically for scraping practice, gathering this sample data is completely authorized and safe.
- **Robots Result:** No robots file found (404 Not Found).

I will not reuse this code on another site without checking its rules and terms first.

## Running the Scraper

### Prerequisites & Lane
This script is built using the **Python / BeautifulSoup** lane. 
Install the dependencies inside a virtual environment:
```bash
pip install requests beautifulsoup4 pydantic
```

### Run Command
```bash
python src/main.py
```

## Architecture & Schema

### Data Schema
We enforce strict data formatting using a Pydantic `Article` model:
- `title` (str)
- `url` (str)
- `price` (str) - e.g. "£51.77"
- `price_gbp` (float) - e.g. 51.77
- `availability` (str)
- `rating` (str)
- `source_page` (str)
- `fetched_at` (float)
- `description` (str, optional)

### Politeness Rules
To be a good netizen, the crawler implements:
- **Identification:** Uses a custom User-Agent (`FlyRankInternshipA9/1.0 (+https://github.com/AllTimeFav/Flyrank_Assignments)`).
- **Delays:** Sleeps for `0.5` seconds between network requests.
- **Timeouts:** Caps requests at `5` seconds to avoid hanging indefinitely.
- **Caching:** Catalogue list pages are locally cached to `cache/` to prevent hammering the server during repetitive testing runs.
- **Error Handling:** Immediately skips 404/403 responses without retrying, preventing harassment.

### Honest Limitation
The script strictly uses a blocking, sequential loop and relies on naive substring checking (`class_='next'`) to find pagination links. It works perfectly for this site but would be too slow to crawl millions of pages and might break if the site's pagination HTML structure changes slightly.

### Why No Browser Was Needed
This assignment did not require a headless browser (like Playwright or Selenium) because all the book data is already present in the static HTML the server sends; rendering a full browser would only add unnecessary computation cost and bandwidth.

## Run Report Proof

Here is the `output/run-report.json` from a successful run containing 60 legitimate book URLs and 1 intentionally injected fake URL to test failure handling:

```json
{
    "start_time": 1787933298.3625035,
    "duration": 102.69312810897827,
    "pages_fetched": 60,
    "cache_hits": 3,
    "valid_records": 60,
    "invalid_records": 0,
    "failed_pages": 1
}
```

## Ethics Statement
When scraping data, always check if an official API exists first—use it if available to save resources for both parties. Never attempt to bypass authentication, logins, paywalls, or anti-bot blocks to steal restricted content. Always respect rate limits and only collect the minimal data necessary for your objective.
