"""Scrape the public practice website books.toscrape.com (educational demo)."""
import argparse
import time
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE = 'https://books.toscrape.com/'
HEADERS = {'User-Agent': 'BI-Portfolio-Educational-Demo/1.0'}
RATINGS = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

def scrape(pages=3):
    records = []
    with requests.Session() as session:
        session.headers.update(HEADERS)
        for page in range(1, pages + 1):
            url = BASE if page == 1 else urljoin(BASE, f'catalogue/page-{page}.html')
            response = session.get(url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.select('article.product_pod')
            if not books:
                break
            for book in books:
                title = book.select_one('h3 a')
                price = book.select_one('.price_color')
                availability = book.select_one('.availability')
                rating = book.select_one('.star-rating')
                records.append({
                    'title': title.get('title', title.get_text(strip=True)) if title else '',
                    'price_gbp': float(price.get_text(strip=True).replace('£', '').replace('Â', '').strip()) if price else None,
                    'rating': next((RATINGS[c] for c in rating.get('class', []) if c in RATINGS), None) if rating else None,
                    'in_stock': bool(availability and 'In stock' in availability.get_text(' ', strip=True)),
                    'product_url': urljoin(url, title['href']) if title else '',
                    'source_page': page,
                })
            time.sleep(0.5)
    return pd.DataFrame(records)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages', type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.pages <= 50:
        parser.error('--pages must be between 1 and 50')
    output = Path(__file__).parent / 'data'
    output.mkdir(exist_ok=True)
    df = scrape(args.pages)
    if df.empty:
        raise RuntimeError('No records found; verify website availability and structure')
    df.to_csv(output / 'raw_books.csv', index=False)
    print(f'Saved {len(df)} records to data/raw_books.csv')

if __name__ == '__main__':
    main()
