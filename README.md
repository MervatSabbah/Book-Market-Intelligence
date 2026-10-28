# Business Intelligence & Web Scraping Portfolio (Demo)

A self-contained **educational demonstration project** showing how publicly accessible practice-site product listings can be collected, validated, transformed, and explored in an interactive analytics dashboard. It does **not** contain employer data, private emails, proprietary code, or confidential material.

## Workflow

`books.toscrape.com` → `scrape.py` (requests + Beautiful Soup) → `data/raw_books.csv` → `pipeline.py` (Pandas) → `data/clean_books.csv` / `data/clean_books.xlsx` → `dashboard.py` (Streamlit + Plotly)

## Features

- Scrapes book titles, GBP prices, star ratings, stock status, product URLs, and source-page numbers.
- Cleans and validates records, removes duplicate URLs, and assigns price bands.
- Interactive dashboard with filters, KPIs, price distribution, rating chart, and CSV download.
- Includes small unit tests for data transformations.

## Run locally

```bash
python -m pip install -r requirements.txt
python scrape.py --pages 3
python pipeline.py
streamlit run dashboard.py
```

The scripts require an internet connection for scraping. The target site is a public **practice website specifically designed for scraping**. Use modest request volumes and comply with site rules. The dashboard runs on the generated local dataset.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Publishing

1. Create a **public** GitHub repository named `bi-scraping-portfolio`.
2. Upload these files and folders, excluding virtual environments and any sensitive information.
3. Run the scripts to generate sample data, if desired, and commit only the public demo data.
4. Share the resulting repository URL in the job application. You can optionally deploy `dashboard.py` via Streamlit Community Cloud after the dataset is committed.

## Ethical disclosure

This is a personal **demonstration project**, not a representation of a past production web-scraping engagement. Professional experience in email extraction and workflow automation using Power Automate is a separate skill set.
