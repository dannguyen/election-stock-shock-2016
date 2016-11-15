# setup up the tables

echo "
.separator ,

DROP TABLE IF EXISTS stock_prices;
CREATE TABLE stock_prices (
    symbol VARCHAR(6) NOT NULL,
    date DATE NOT NULL,
    closing_price FLOAT NOT NULL,
    volume INTEGER NOT NULL
);

DROP TABLE IF EXISTS companies;
CREATE TABLE companies (
    symbol VARCHAR(6) NOT NULL,
    name VARCHAR(255) NOT NULL,
    last_sale FLOAT NOT NULL,
    market_cap FLOAT NOT NULL,
    ipo_year INTEGER,
    sector VARCHAR(255),
    sub_industry VARCHAR(255),
    nasdaq_url VARCHAR(255) NOT NULL
);


DROP TABLE IF EXISTS sp500;
CREATE TABLE sp500 (
    symbol VARCHAR(6) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    sector VARCHAR(255) NOT NULL,
    sub_industry VARCHAR(255) NOT NULL,
    date_first_added DATE,
    cik VARCHAR(20) NOT NULL
);


.import wrangled/stock_prices.csv stock_prices
.import wrangled/companies.csv companies
.import wrangled/sp500.csv sp500

CREATE INDEX sp500_on_symbol ON sp500(symbol);
CREATE INDEX sp500_on_sector ON sp500(sector);
CREATE INDEX sp500_on_sub_industry ON sp500(sub_industry);


CREATE INDEX companies_on_symbol ON sp500(symbol);
CREATE INDEX companies_on_sector ON sp500(sector);
CREATE INDEX companies_on_sub_industry ON sp500(sub_industry);

CREATE INDEX stock_prices_on_symbol_and_date
    ON stock_prices(symbol, date);
CREATE INDEX stock_prices_on_date
    ON stock_prices(date);" \
    | sqlite3 wrangled/stock_shock.sqlite




