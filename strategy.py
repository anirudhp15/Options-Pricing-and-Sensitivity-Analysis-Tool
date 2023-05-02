import pandas as pd
from datetime import datetime
import yfinance as yf

def main():
    # Output the results
    print("Cumulative Returns:")
    print(cumulative_returns.tail())

def get_prices(tickers, start_date, end_date):
    prices = pd.DataFrame()
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        prices[ticker] = data['Adj Close']
    return prices

def mean_reversion_strategy(prices, threshold):
    signals = pd.DataFrame(columns=prices.columns)
    for i in range(1, len(prices)):
        prev_prices = prices.iloc[i-1]
        curr_prices = prices.iloc[i]
        z_scores = (curr_prices - prev_prices.mean()) / prev_prices.std()
        buy_signals = z_scores < -threshold
        sell_signals = z_scores > threshold
        signals.loc[curr_prices.name] = 0
        signals.loc[curr_prices.name, buy_signals] = 1
        signals.loc[curr_prices.name, sell_signals] = -1
    return signals

# Example usage:
tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN']  # S&P 500 equities to trade
start_date = '2015-01-01'  # Start date of historical price data
end_date = datetime.today()    # End date of historical price data
threshold = 2.0  # Z-score threshold for trading signals

# Get historical price data for the selected equities
prices = get_prices(tickers, start_date, end_date)

# Implement the mean-reversion trading strategy
signals = mean_reversion_strategy(prices, threshold)

# Calculate daily returns based on the trading signals
daily_returns = signals.shift(1) * (prices - prices.shift(1)) / prices.shift(1)

# Calculate cumulative returns over the backtest period
cumulative_returns = (1 + daily_returns).cumprod() - 1

if __name__ == "__main__":
    main()
