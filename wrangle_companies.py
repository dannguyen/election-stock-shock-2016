from pathlib import Path
import csv
import re
SRC = {
    'nasdaq': Path('companylists', 'nasdaq.csv'),
    'nyse': Path('companylists', 'nyse.csv'),
    'sp500': Path('companylists', 'sp500.csv'),
}

DEST_DIR =  Path('wrangled')
COMPANY_HEADERS = ["symbol","name","last_sale","market_cap","ipo_year",
                        "sector","sub_industry","nasdaq_url"]


dest_companies = DEST_DIR.joinpath('companies.csv')

with dest_companies.open('w') as wf:
    wcsv = csv.DictWriter(wf, fieldnames=COMPANY_HEADERS)
    wcsv.writeheader()
    rows = list(csv.DictReader(SRC['nasdaq'].read_text().replace('n/a', '').splitlines()))
    rows.extend(csv.DictReader(SRC['nyse'].read_text().replace('n/a', '').splitlines()))

    # remove all listings that have a carat in their ticker, i.e.
    # "MITT^A"
    cleanedrows = [r for r in rows if '^' not in r["Symbol"] and re.search('B|M', r['MarketCap'])]

    print("Number of companies to write:", len(cleanedrows))
    for row in cleanedrows:
        r = {k: row[k].strip() for k, v in row.items()}
        x = {}
        x['symbol'] = r['Symbol']
        x['name'] = r['Name']
        x['last_sale'] = r['LastSale']
        # convert {"MarketCap": "$1.61B"}
        # to {'market_cap': 1610000000}
        mc, mult = re.search(r'(?<=\$)([0-9.]+)(B|M)', r['MarketCap']).groups()
        x['market_cap'] = float(mc) * 1000000000 if mult == 'B' else float(mc) * 1000000
        x['ipo_year'] = r['IPOyear']
        x['sector'] = r['Sector']
        x['sub_industry'] = r['industry']
        x['nasdaq_url'] = r['Summary Quote']
        wcsv.writerow(x)


