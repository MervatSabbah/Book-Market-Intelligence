"""Validate and transform scraped public demo records."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).parent / 'data'

def transform(df):
    required = {'title', 'price_gbp', 'rating', 'in_stock', 'product_url', 'source_page'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    result = df.copy()
    result['price_gbp'] = pd.to_numeric(result['price_gbp'], errors='coerce')
    result['rating'] = pd.to_numeric(result['rating'], errors='coerce')
    result = result.dropna(subset=['title', 'price_gbp'])
    result = result[result['price_gbp'].ge(0) & result['rating'].between(1, 5)]
    result = result.drop_duplicates(subset=['product_url'])
    result['price_band'] = pd.cut(result['price_gbp'], bins=[-0.01, 20, 40, float('inf')], labels=['Budget', 'Mid-range', 'Premium'])
    return result.sort_values(['price_gbp', 'title']).reset_index(drop=True)

def main():
    DATA.mkdir(exist_ok=True)
    source = DATA / 'raw_books.csv'
    if not source.exists():
        raise SystemExit('Run python scrape.py first to collect source data.')
    cleaned = transform(pd.read_csv(source))
    cleaned.to_csv(DATA / 'clean_books.csv', index=False)
    cleaned.to_excel(DATA / 'clean_books.xlsx', index=False)
    print(f'Processed {len(cleaned)} books; exported CSV and Excel')

if __name__ == '__main__':
    main()
