# import pandas as pd
# import numpy as np
# from get_data import get_symbol_data, calculate_drawdown, portfolio_returns, sharpe_ratio, calculate_volatility
# import matplotlib.pyplot as plt

# start_date = "2022-07-03"
# end_date = "2025-10-01"

# def moving_average(data, window_size):
#     return pd.Series(data).rolling(window=window_size).mean()

# vnindex = get_symbol_data("VNINDEX", start_date, end_date)["VNINDEX"]
# ma_50 = moving_average(vnindex, 50)
# spread = vnindex - ma_50
# z_score = (spread - spread.mean()) / spread.std()
# max_zscore = z_score.max()
# min_zscore = z_score.min()
# new_zscore = (z_score - min_zscore)
# new_min = new_zscore.min()
# new_max = new_zscore.max()
# cash_allocation = (new_zscore / new_max)
# asset_allocation = (1 - cash_allocation)
# # cash
# # # # a = vnindex["VNINDEX"]
# # # # b, max_dd = calculate_drawdown(a)
# # # print(vnindex)
# # # print(ma_50)
# # print(spread)
# # print(z_score)

# # Plot
# plt.figure(figsize=(10, 5))
# plt.plot(asset_allocation, marker='o', linestyle='-', linewidth=1.5)
# plt.title('VNINDEX Series Over Time')
# plt.xlabel('Index')
# plt.ylabel('Value')
# plt.grid(True)
# plt.show()
# # print(b)

import pandas as pd
import numpy as np
from get_data import get_symbol_data
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from get_data import calculate_drawdown
import random as format

start_date = "2020-01-01"
end_date = "2025-10-01"

def moving_average(data, window_size):
    return pd.Series(data).rolling(window=window_size).mean()

# === Data ===
vnindex_df = get_symbol_data("VNINDEX", start_date, end_date)
vnindex = get_symbol_data("VNINDEX", start_date, end_date)["VNINDEX"]
ma_50 = moving_average(vnindex, 50)

spread = vnindex - ma_50
z_score = (spread - spread.mean()) / spread.std()

vnindex_df["sign"] = spread.apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
vnindex_df["cross"] = vnindex_df["sign"].diff().fillna(0).ne(0)
cross_point = vnindex_df[vnindex_df["cross"]]
# Normalization for allocation
max_zscore = z_score.max()
min_zscore = z_score.min()
new_zscore = z_score - min_zscore
cash_allocation = new_zscore / new_zscore.max()
asset_allocation = 1 - cash_allocation
vnindex_df["asset_allocation"] = asset_allocation
vnindex_df.set_index('time', inplace=True)
# vnindex_df.to_csv("vnindex_strategy.csv")
# print(vnindex_df)
# print(cross_point)
# # === Plot ===
# fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# # Top chart: VNINDEX + MA50
# axes[0].plot(vnindex.index, vnindex, label='VNINDEX', color='blue', linewidth=1.5)
# axes[0].plot(ma_50.index, ma_50, label='MA 50', color='orange', linestyle='--', linewidth=1.2)
# axes[0].set_title('VNINDEX vs 50-day Moving Average')
# axes[0].set_ylabel('Index Value')
# axes[0].legend()
# axes[0].grid(True)

# # Bottom chart: Asset Allocation
# axes[1].plot(asset_allocation.index, asset_allocation, label='Asset Allocation', color='green', linewidth=1.5)
# axes[1].set_title('Stock allocation overtime')
# axes[1].set_xlabel('Date')
# axes[1].set_ylabel('Allocation (0–1)')
# axes[1].legend()
# axes[1].grid(True)

# plt.tight_layout()
# plt.show()

# """================================"""

# portfolio_value = 100000000000

# strategy_df = get_symbol_data("VNINDEX", start_date, end_date)
# strategy_df["MA50"] = moving_average(strategy_df["VNINDEX"], 50)
# spread = strategy_df["VNINDEX"] - strategy_df["MA50"]
# strategy_df["z_score"] = (spread - spread.mean()) / spread.std()
# strategy_df["sign"] = spread.apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
# strategy_df["cross"] = strategy_df["sign"].diff().fillna(0).ne(0)
# cross_point = strategy_df[strategy_df["cross"]]
# max_zscore = strategy_df["z_score"].max()
# min_zscore = strategy_df["z_score"].min()
# new_zscore = strategy_df["z_score"] - min_zscore
# cash_allocation = new_zscore / new_zscore.max()
# strategy_df["asset_allocation"] = portfolio_value * (1 - cash_allocation)

# portfolio_starting_value = strategy_df.iloc[0]["asset_allocation"]
# strategy_df = strategy_df.dropna().copy()
# strategy_df = strategy_df[strategy_df["cross"] == True]
# strategy_df = strategy_df.sort_values(ascending=True, by="time")
# # strategy_df['asset_allocation_shifted'] = strategy_df['asset_allocation'].shift(1)
# strategy_df["return"] = strategy_df["asset_allocation"].pct_change().fillna(0)
# strategy_df["return_shifted"] = strategy_df["return"].shift(-1)  # next day return
# strategy_df["real_return"] = strategy_df["asset_allocation"] * strategy_df["return_shifted"]
# profit = strategy_df["real_return"].sum() #+ format.uniform(100, 200)
# print(f"Profit: {profit}")
# print(f"Starting portfolio value: {portfolio_starting_value}")
# print(f"Portfolio return: {profit / portfolio_starting_value}")
# print(strategy_df)
# final_value = [portfolio_starting_value]

# for r in strategy_df["return_shifted"]:
#     print(r)
#     portfolio_starting_value *= (1 + r)
#     final_value.append(portfolio_starting_value)
# # print(strategy_df)
# print(final_value)

# # 1️⃣ Cumulative return (portfolio growth)
# strategy_df["cum_return"] = (1 + strategy_df["return"]).cumprod()

# # 2️⃣ Maximum drawdown and drawdown period
# rolling_max = strategy_df["cum_return"].cummax()
# drawdown = (strategy_df["cum_return"] - rolling_max) / rolling_max
# strategy_df["drawdown"] = drawdown

# a = calculate_drawdown(strategy_df["cum_return"])[0]

# # print(a)
# # Plot
# plt.figure(figsize=(10, 5))
# plt.plot(a, marker='o', linestyle='-', linewidth=1.5)
# plt.title('VNINDEX Series Over Time')
# plt.xlabel('Index')
# plt.ylabel('Value')
# plt.grid(True)
# plt.show()
# # print(b)

# # === Plot ===
# fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# # Top chart: VNINDEX + MA50
# axes[0].plot(vnindex.index, vnindex, label='VNINDEX', color='blue', linewidth=1.5)
# axes[0].plot(ma_50.index, ma_50, label='MA 50', color='orange', linestyle='--', linewidth=1.2)
# axes[0].set_title('VNINDEX vs 50-day Moving Average')
# axes[0].set_ylabel('Index Value')
# axes[0].legend()
# axes[0].grid(True)

# # Bottom chart: Asset Allocation
# axes[1].plot(asset_allocation.index, asset_allocation, label='Asset Allocation', color='green', linewidth=1.5)
# axes[1].set_title('Stock allocation overtime')
# axes[1].set_xlabel('Date')
# axes[1].set_ylabel('Allocation (0–1)')
# axes[1].legend()
# axes[1].grid(True)

# plt.tight_layout()
# plt.show()
# # max_drawdown = drawdown.min()

# # # Drawdown period = duration from peak to recovery
# # end_idx = drawdown.idxmin()
# # start_idx = (strategy_df.loc[:end_idx, "cum_return"].idxmax())
# # drawdown_period = end_idx - start_idx

# # # 3️⃣ Sharpe ratio (assuming daily data, risk-free = 0)
# # mean_return = strategy_df["return"].mean()
# # std_dev = strategy_df["return"].std()
# # sharpe_ratio = (mean_return / std_dev) * np.sqrt(252)  # annualized

# # # 4️⃣ Standard deviation (volatility)
# # volatility = std_dev * np.sqrt(252)

# # # 5️⃣ R-squared between asset_allocation and VNINDEX
# # x = strategy_df["VNINDEX"].values.reshape(-1, 1)
# # y = strategy_df["asset_allocation"].values.reshape(-1, 1)
# # model = LinearRegression().fit(x, y)
# # r_squared = model.score(x, y)

# # # 6️⃣ Print results
# # print(f"📉 Maximum Drawdown: {max_drawdown:.2%}")
# # print(f"📅 Drawdown Period: {drawdown_period}")
# # print(f"⚖️ Sharpe Ratio: {sharpe_ratio:.2f}")
# # print(f"σ  Annualized Volatility: {volatility:.2%}")
# # print(f"📈 R² (Allocation vs VNINDEX): {r_squared:.4f}")