# Stock Evaluator

This project implements the Iron Condor trading strategy using the Polygon API to retrieve stock and options data.

## Table of Contents
   - [Setup Instructions](#setup-instructions)
   - [Project Milestones](#project-milestones)
   - [Documentation](#documentation)

## Setup Instructions

### Cloning the Repo
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/polygon-iron-condor.git
2. To make api request, you must first need an account with polygon and retrieve your own api token. This will shown upon creation.
3. Create a config directory and a file name called secrets.properties. Follow the convention below:
   ```bash
   [DEFAULT]
   POLYGON_API_KEY=secret

### Installing/setup postgreSQL
#### Windows
1. Download and install PostgreSQL from the [official PostgreSQL download page](https://www.postgresql.org/download/windows/).
2. During the installation, ensure you install the following components:
   - PostgreSQL Server
   - SQL Shell (psql)
3. In sql shell (psql)
   - You'll be prompt to create the server location. We will be taking the default as this is only for a local environment.
   ```bash
   Server [localhost]: 
   Database [postgres]: 
   Port [5432]: 
   Username [postgres]: 
   Password for user postgres: <Enter the password you set during installation>
   ```
   - We then create a new database:
   ```bash
   CREATE DATABASE stock_data;
   ```
   - Switch to the new table:
   ```bash
   \c stock_data
   ```
   - Create the stock_prices table with appropriate schema
   ```bash
   CREATE TABLE stock_prices (id SERIAL PRIMARY KEY, ticker VARCHAR(10) NOT NULL, date DATE NOT NULL, open_price FLOAT NOT NULL, close_price FLOAT NOT NULL, high_price FLOAT NOT NULL, low_price FLOAT NOT NULL, volume FLOAT NOT NULL, vwap FLOAT, adjusted BOOLEAN, UNIQUE(ticker, date));
   ```
   - We add the indexing for faster querying of the stock data. We add indexing on ticker and date columns. 
   ```bash
   CREATE INDEX idx_ticker_date ON stock_prices(ticker, date);
   ```
   - Click [here](#table-structure-and-explanation) for documentation on how we determined the values for this table and why
   - To check if you successfully made the table:
   ```bash
   IF YOU HAVENT ALREADY, OPEN SHELL AND CONNECT TO THE DATABASE WHERE YOU CREATED THE TABLE:
   psql -U postgres -d stock_data

   TO LIST THE LIST OF RELATIONS:
   stock_data-# \dt
               List of relations
   Schema |     Name     | Type  |  Owner
   --------+--------------+-------+----------
   public | stock_prices | table | postgres
   (1 row)

   stock_data-# \d stock_prices
                                       Table "public.stock_prices"
      Column    |         Type          | Collation | Nullable |                 Default
   -------------+-----------------------+-----------+----------+------------------------------------------
   id          | integer               |           | not null | nextval('stock_prices_id_seq'::regclass)
   ticker      | character varying(10) |           | not null |
   date        | date                  |           | not null |
   open_price  | double precision      |           | not null |
   close_price | double precision      |           | not null |
   high_price  | double precision      |           | not null |
   low_price   | double precision      |           | not null |
   volume      | double precision      |           | not null |
   vwap        | double precision      |           |          |
   adjusted    | boolean               |           |          |
   Indexes:
      "stock_prices_pkey" PRIMARY KEY, btree (id)
      "idx_ticker_date" btree (ticker, date)
      "stock_prices_ticker_date_key" UNIQUE CONSTRAINT, btree (ticker, date)
   ```

## Project Milestones
1. Set up back-end.
   - ~~Create a envrionment with initial api get method utilizing a ticker and two dates.~~
   - Data storage
      - Stored in sql.
         - We are using **PostgreSQL**
         - Create a basic table grabbing some data off of the API call for a single stock and it's date.
      - How do we do data rotation(data persistence)?
         - How long a piece of data stays into storage?
         - Do we need temporary data for on the go analysis? 
         - We want to retain a log tracking progression on an option call and its price points. This should be updated after market is closed so once per day. 
      - We need to gather option chains from the Polygon api
         - Data includes the following:
            - Strike prices
            - Expiration Dates
            - Implied volatility
            - Bid/Ask Prices
            - Open interest
            - Greeks (Delta, Gamma, Vega, Theta)
      - Need to make a position data storage where we input the contracts we bought and when. 
         - Eventually make a notification on if to sell or not. 
      
2. Set up evaluation logic. 
   - There's a few key things here. I want to keep track of stocks that may go up or may go down, on top of that the theta or options degredation. 

   - Research the option trading strategies and come up with a conclusion. 
   - Research stop loss
   - Research Options
      -Theta Decay

## Documentation

### SQL 
#### Table Structure and Explanation

1. **id SERIAL PRIMARY KEY**
   - **Type**: `SERIAL`
   - **Explanation**: This is an auto-incrementing integer, which acts as the unique identifier for each record. The `PRIMARY KEY` ensures that each record has a unique ID.

2. **ticker VARCHAR(10)**
   - **Type**: `VARCHAR(10)`
   - **Explanation**: The stock ticker symbol (e.g., 'AAPL'). This can be up to 10 characters in length, which is sufficient for most ticker symbols.

3. **date DATE**
   - **Type**: `DATE`
   - **Explanation**: This field stores the date of the stock data entry. It's important for tracking historical data and performing time-series analysis.

4. **open_price FLOAT**
   - **Type**: `FLOAT`
   - **Explanation**: The price at which the stock opened on the given date. We use `FLOAT` for fractional precision, as stock prices are often not whole numbers.

5. **close_price FLOAT**
   - **Type**: `FLOAT`
   - **Explanation**: The price at which the stock closed on the given date. Like the `open_price`, this is stored as a `FLOAT` for precision.

6. **high_price FLOAT**
   - **Type**: `FLOAT`
   - **Explanation**: The highest price the stock reached during the trading day. `FLOAT` is used to store fractional values with precision.

7. **low_price FLOAT**
   - **Type**: `FLOAT`
   - **Explanation**: The lowest price the stock reached during the trading day. This value is crucial for analyzing the volatility of the stock.

8. **volume FLOAT**
   - **Type**: `FLOAT`
   - **Explanation**: The trading volume, representing how many shares were traded during the day. Volume is important for assessing the liquidity of the stock and the strength of price movements.

9. **vwap FLOAT**
   - **Type**: `FLOAT`
   - **Explanation**: Volume-weighted average price (VWAP), which provides a measure of the average price weighted by volume. It's often used as a benchmark for price analysis.

10. **adjusted BOOLEAN**
    - **Type**: `BOOLEAN`
    - **Explanation**: This field indicates whether the stock prices are adjusted for splits or dividends. Adjusted prices help provide a consistent historical comparison of stock performance.


