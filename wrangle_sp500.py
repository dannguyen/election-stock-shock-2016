from datetime import date
from pathlib import Path
import csv
import re
SRC = Path('companylists', 'sp500.csv')
DEST = Path('wrangled', 'sp500.csv')

rcsv = csv.DictReader(SRC.read_text().splitlines())

with DEST.open('w') as wf:
    wcsv = csv.DictWriter(wf, fieldnames=rcsv.fieldnames)
    wcsv.writeheader()
    for row in rcsv:
        x = {k: row[k].strip() for k, v in row.items()}
        datestr = re.search('^(\d+)/(\d+)/(\d+)', row['date_first_added'])
        if datestr:
            month, day, year = [int(i) for i in datestr.groups()]
            year = year + 2000 if year < 16 else year + 1900
            x['date_first_added'] = date(year, month, day).isoformat()
        else:
            x['date_first_added'] = None
        wcsv.writerow(x)



