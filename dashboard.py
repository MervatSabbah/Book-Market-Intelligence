"""Interactive analytics dashboard for educational web scraping data."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Book Market Intelligence | Demo', layout='wide')
st.title('Book Market Intelligence')
st.caption('Educational portfolio demo | Public practice website: books.toscrape.com | Not live commercial data')
path = Path(__file__).parent / 'data' / 'clean_books.csv'
if not path.exists():
    st.warning('Run scrape.py and pipeline.py to generate the dataset.')
    st.stop()
df = pd.read_csv(path)
selected = st.sidebar.multiselect('Price band', sorted(df['price_band'].dropna().unique()), default=sorted(df['price_band'].dropna().unique()))
filtered = df[df['price_band'].isin(selected)]
a, b, c, d = st.columns(4)
a.metric('Books', f'{len(filtered):,}')
b.metric('Average price', f"£{filtered['price_gbp'].mean():.2f}" if not filtered.empty else 'N/A')
c.metric('Average rating', f"{filtered['rating'].mean():.2f} / 5" if not filtered.empty else 'N/A')
d.metric('In-stock share', f"{filtered['in_stock'].mean():.0%}" if not filtered.empty else 'N/A')
if not filtered.empty:
    left, right = st.columns(2)
    with left:
        st.plotly_chart(px.histogram(filtered, x='price_gbp', nbins=15, title='Price distribution', labels={'price_gbp': 'Price (GBP)'}), use_container_width=True)
    with right:
        counts = filtered.groupby('rating').size().reset_index(name='books')
        st.plotly_chart(px.bar(counts, x='rating', y='books', title='Books by rating'), use_container_width=True)
st.subheader('Filtered dataset')
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button('Download filtered CSV', filtered.to_csv(index=False), file_name='filtered_books.csv', mime='text/csv')
