from pathlib import Path
import csv
import re
SRCGLOB = Path('yahoofinance').glob('*.csv')
DEST = Path('wrangled', 'stock_prices.csv')

DEST_HEADERS = ['symbol', 'date', 'closing_price', 'volume']

data = []
for src in SRCGLOB:
    symbol = src.stem
    txt = src.read_text()
    if 'html' not in txt and re.match('^[A-Z]+$', symbol):
        for r in csv.DictReader(txt.splitlines()):
            x = {'symbol': symbol,
                'date': r['Date'], 'volume': r['Volume'],
                 'closing_price': round(float(r['Adj Close']), 2 )}
            data.append(x)



with DEST.open('w') as wf:
    print("Writing to:", DEST)
    wcsv = csv.DictWriter(wf, fieldnames=DEST_HEADERS)
    wcsv.writeheader()
    wcsv.writerows(sorted(data, key=lambda x: (x['symbol'], x['date'])))
