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
2. Set up iron condor logic. 
   - Research the iron condor strategy process data and gives its conclusion. 
   - Research stop loss
   - Research Options
      -Theta Decay

## Documentation

### Iron Condor Lifecycle (30 - 45 Days Before Expiration)

The 30 to 45 days before expiration period is often considered the **sweet spot** for Iron Condor and other options strategies because it provides an ideal balance between risk and reward, specifically in terms of **time decay (theta)** and managing volatility. Here’s a breakdown of the lifecycle of an Iron Condor strategy, revolving around this time period:

#### Iron Condor Lifecycle (30-45 Days Before Expiration)

#### 1. **Setup (Day 0: 30-45 Days Before Expiration)**
   - **Action**: You enter the Iron Condor trade by selling a call and a put option close to the current stock price and buying a call and a put further out of the money to cap your risk. The goal is for the underlying stock price to remain between the strike prices of the options sold, allowing the options to expire worthless.
   - **Reason for 30-45 Days**: This period captures the best balance between collecting option premium and minimizing the risks associated with high volatility near expiration. The options still have significant extrinsic value at this point, but time decay is starting to accelerate.
   - **Theta Decay**: The closer you are to expiration, the faster the time value of the options decays. Entering 30-45 days out allows you to capitalize on the rapid acceleration of time decay as expiration nears.
   
   **Key Tasks**:
   - **Select Strike Prices**: Choose strike prices far enough from the current stock price to reduce the risk of the stock hitting those prices.
   - **Monitor Volatility**: Ensure implied volatility is relatively high when entering, as this increases the premium you receive from selling options.
   - **Maximizing Premium**: Focus on selling options with higher premiums due to volatility, while keeping the strike prices far enough to minimize the risk of early assignment or major price movement.

#### 2. **Monitoring and Adjustments (Day 1 to Day 30: 15-30 Days Before Expiration)**
   - **Action**: After the trade is set up, regular monitoring is essential. The goal is to watch how the stock price moves in relation to the strike prices and manage the trade if needed. You generally don’t want to make drastic changes unless the underlying price moves too close to one of the strike prices.
   - **Time Decay**: During this phase, time decay starts working in your favor. As days pass, the options lose value because the likelihood of the stock price hitting one of the strike prices decreases. 
   - **Adjustment Scenarios**:
     - **Stock Near Strike Price**: If the stock price is approaching one of the strike prices, you may want to adjust the position by rolling the untested side closer to the current price to capture more premium.
     - **Volatility Changes**: If implied volatility drops significantly, you can potentially close the trade early for a profit since the price of the options will drop faster.
   - **Profit Target**: Many traders aim to capture **50-75% of the maximum potential profit** during this period and exit early to avoid the higher risks that come as expiration approaches.

   **Key Tasks**:
   - **Track Price Movement**: Monitor how the underlying stock’s price moves in relation to your strike prices.
   - **Adjust the Trade**: If necessary, adjust the untested side of the Iron Condor or roll the entire position to a later expiration date.
   - **Exiting Early**: If you have captured a large portion of the premium (e.g., 50-75%), consider closing the position early to lock in profits and reduce risk.

#### 3. **Final Monitoring (Day 31 to Day 40: 5-10 Days Before Expiration)**
   - **Action**: As you approach the final 5-10 days before expiration, this is the critical decision point for whether to hold the Iron Condor to expiration or close it early. The key is to assess how close the underlying stock price is to the strike prices of the sold options.
   - **Time Decay at Its Peak**: Time decay is now at its most rapid. If the stock price is within your desired range (between the sold strikes), most of the premium will have decayed, and you may have already captured most of the potential profit.
   - **Avoid Assignment Risk**: While you can continue holding the Iron Condor, many traders choose to exit before expiration to avoid assignment risk. If the stock price is near one of your strike prices, there is a risk of the short option being exercised, leading to significant losses.

   **Key Tasks**:
   - **Assess Risk**: Determine whether the stock price is still comfortably within the sold strike prices. If it’s getting too close, consider closing the trade early.
   - **Profit Locking**: If you’ve captured the majority of the premium, consider closing the position to avoid the risk of last-minute volatility or market events (e.g., earnings reports, economic data) that could move the stock sharply.
   - **Avoiding Expiration Risk**: If the stock price is near the strike price of one of your sold options, it’s generally safer to close the position rather than risk being assigned the underlying stock.

#### 4. **Expiration (Day 41 to Day 45: 0-5 Days Before Expiration)**
   - **Action**: This is the final stage of the Iron Condor lifecycle. If the trade is held until expiration and the stock remains between the strike prices of the options sold, the options will expire worthless, and you can keep the full premium.
   - **Final Profits**: If everything goes as planned and the stock remains within the sold strike prices, you will capture the full premium of the trade. The closer you are to expiration, the less premium remains, so you must decide whether the remaining risk justifies holding the trade.
   - **Assignment Risk**: If the stock price crosses the strike prices of either the call or put options sold, you could face assignment, meaning you would be obligated to sell or buy the underlying stock. Many traders prefer to close the position before this point to avoid this.

   **Key Tasks**:
   - **Let Expire or Close**: If the stock remains comfortably within the strike prices, you can let the options expire worthless. If the stock price nears one of the sold strikes, consider closing the position to avoid assignment.
   - **Final Risk Management**: Assess whether any sudden market events or changes in volatility could affect the outcome in the last few days. If there’s a risk of assignment, close the position.

### Example Lifecycle Scenario

#### Day 0 (Setup):
- **Underlying Stock**: XYZ is trading at $100.
- **Iron Condor Setup**: You sell a call at $110, buy a call at $115, sell a put at $90, and buy a put at $85. This gives you a price range between $90 and $110 where you expect the stock to remain.
- **Expiration**: 45 days away.
- **Premium Collected**: You collect $200 in premium.

#### Day 10-35 (Monitoring):
- **Stock Movement**: The stock stays between $92 and $108 over the next few weeks, so there’s no need for major adjustments. The options start losing value due to time decay.
- **Profit Target**: By day 30, the options have lost most of their time value, and you’ve captured 70% of the premium.
- **Action**: You could choose to close the trade at this point and lock in $140 of profit.

#### Day 36-40 (Final Monitoring):
- **Stock Movement**: The stock is now trading at $108, getting close to the $110 strike price of the sold call. You monitor closely to see if the stock moves closer to $110.
- **Action**: If the stock remains near $108 but doesn’t cross $110, you could hold until expiration or close the position to lock in your gains and avoid any last-minute volatility.

#### Day 41-45 (Expiration):
- **Stock Movement**: The stock closes at $107 on expiration day, and all options expire worthless. You keep the full $200 in premium.
- **Action**: If the stock had moved closer to $110, you might have closed the position a day or two earlier to avoid assignment risk.

### Why This 30-45 Day Period Works

- **Optimal Time Decay**: In this period, the time decay of options accelerates significantly, meaning the premium collected for selling options decays quickly, giving you more potential profit without holding the trade for too long.
- **Manageable Volatility**: 30-45 days out from expiration typically sees less volatility than the final week before expiration, allowing you to monitor and adjust positions with lower risk.
- **Adjustment Opportunity**: If the trade moves against you early in the lifecycle, you have time to adjust or roll the trade without getting too close to expiration, where options tend to become more sensitive to price movements.

### Conclusion:
Revolving your Iron Condor strategy around the **30-45 days before expiration** window maximizes the benefits of time decay and minimizes risk from sharp price movements or unexpected volatility close to expiration. Regular monitoring, adjustments, and early exits at the right time will help you capture profits and avoid unnecessary risks.


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


