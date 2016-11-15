from pathlib import Path
from copy import copy
import requests
import csv
from time import sleep
DEST_DIR = Path('yahoofinance')
DEST_DIR.mkdir(exist_ok=True)

BASE_URL = 'http://chart.finance.yahoo.com/table.csv'
BASE_URL_PARAMS = {
    'a': 0,
    'b': 1,
    'c': 2016,
    'd': 10,
    'e': 14,
    'f': 2016,
    'ignore': 'csv'
}


def get_data(symbol):
    myparams = copy(BASE_URL_PARAMS)
    myparams['s'] = symbol
    resp = requests.get(BASE_URL, params=myparams)
    return resp.text



if __name__ == '__main__':
    companies = list(csv.DictReader(Path('wrangled', 'companies.csv').read_text().splitlines()))
    companies.sort(key=lambda r: r['symbol'])
    print("Companies in companies.csv:", len(companies))
    for row in companies:
        symbol = row['symbol']
        destpath = DEST_DIR.joinpath("%s.csv" % symbol)

        if not destpath.exists():
            print("Getting", destpath)
            txt = get_data(symbol)
            destpath.write_text(txt)
            print("\t\tWrote %s bytes" % len(txt))
            sleep(0.3)
