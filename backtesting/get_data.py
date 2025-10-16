from vnstock_data import Quote
import pandas as pd
import matplotlib.pyplot as plt



def get_symbol_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    quote = Quote(source='vnd', symbol=symbol)
    df = quote.history(start=start_date, end=end_date, interval="1D")
    
    if df is None or df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")
    
    df = df[["time", "close"]].copy()
    df.rename(columns={"close": symbol}, inplace=True)
    
    return df

def calculate_drawdown(series: pd.Series) -> pd.Series:
    """Calculate the drawdown of a time series."""
    pct_change = series.pct_change().fillna(0)
    positive = pct_change
    # Make the new series
    result = []
    current_val = 0

    for val in positive:
        if val > 0:
            current_val = 0   # reset to zero when s1 > 0
        else:
            current_val = val  # keep the negative or zero values
        result.append(current_val)

    drawdown = pd.Series(result, name="filtered_VNINDEX")
    # print(drawdown)
    max_drawdown = drawdown.max()
    return drawdown, max_drawdown

def portfolio_returns(series: pd.Series, threshold: float = 0.02) -> pd.Series:
    """Calculate portfolio returns based on drawdown threshold."""
    first_day = series.iloc[0]
    last_day = series.iloc[-1]
    total_return = (last_day - first_day) / first_day
    daily_return = total_return / len(series)
    weekly_return = daily_return * 5
    monthly_return = daily_return * 22
    return total_return, daily_return, weekly_return, monthly_return

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.01) -> float:
    """Calculate the Sharpe ratio of a returns series."""
    excess_returns = returns - risk_free_rate / 252  # Assuming 252 trading days
    return excess_returns.mean() / excess_returns.std() * (252 ** 0.5)

def calculate_volatility(series: pd.Series) -> float:
    """Calculate the annualized volatility of a returns series."""
    std = series.std()
    return std

# a = get_symbol_data("VNINDEX")
# b = calculate_drawdown(a["VNINDEX"])[0]
# # print(b)

# # Plot
# plt.figure(figsize=(10, 5))
# plt.plot(b, marker='o', linestyle='-', linewidth=1.5)
# plt.title('VNINDEX Series Over Time')
# plt.xlabel('Index')
# plt.ylabel('Value')
# plt.grid(True)
# plt.show()
# # print(b)