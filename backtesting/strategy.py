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

start_date = "2022-07-03"
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

print(vnindex_df)
print(cross_point)
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
