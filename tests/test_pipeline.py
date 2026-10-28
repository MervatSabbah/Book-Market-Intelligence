import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import transform

class PipelineTests(unittest.TestCase):
    def test_deduplicate_and_price_band(self):
        df = pd.DataFrame([
            {'title': 'A', 'price_gbp': 15, 'rating': 4, 'in_stock': True, 'product_url': 'a', 'source_page': 1},
            {'title': 'A', 'price_gbp': 15, 'rating': 4, 'in_stock': True, 'product_url': 'a', 'source_page': 1},
            {'title': 'B', 'price_gbp': 55, 'rating': 5, 'in_stock': False, 'product_url': 'b', 'source_page': 1},
        ])
        output = transform(df)
        self.assertEqual(len(output), 2)
        self.assertEqual(list(output['price_band'].astype(str)), ['Budget', 'Premium'])

if __name__ == '__main__':
    unittest.main()
