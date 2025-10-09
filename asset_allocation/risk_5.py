import sys
import os
# Add root path to access index_constructor.py
sys.path.append(os.path.abspath("../"))

import numpy as np
import pandas as pd
from vnstock_data import Quote
from asset_allocation.function import calculate_threshold, percentage_position
from regime.checker import regime_changed_date

path = "clean_data/trading_data.csv"

sell_spread = pd.read_csv(path)
sell_spread['date'] = pd.to_datetime(sell_spread['date']).dt.date
sell_spread.sort_values(by='date', inplace=True)
sell_spread.dropna(inplace=True)

""" Refine VNI data """
first_day = sell_spread['date'].iloc[0]
last_day = sell_spread['date'].iloc[-1]
quote = Quote(source='vnd', symbol="VNINDEX")
vnindex = quote.history(start=f"{first_day}", end=f"{last_day}", interval="1D")
vnindex = vnindex[["time", "close"]]
vnindex['time'] = pd.to_datetime(vnindex['time']).dt.date
vnindex = vnindex.rename(columns={"close": "vnindex", "time": "date"})

""" Total market cap & outstanding share """
path = 'asset_allocation/outstanding_with_close.csv'
outstanding_share = pd.read_csv(path)
outstanding_share['market_cap'] = outstanding_share['close'] * outstanding_share['so_cp_luu_hanh']
total_market_cap = outstanding_share['market_cap'].sum()
total_outstanding_share = outstanding_share['so_cp_luu_hanh'].sum()

""" Merge & calculate """
merge = pd.merge(sell_spread, vnindex, on='date')
merge.set_index('date', inplace=True)
merge = merge.loc[regime_changed_date:] #"2025-07-25"
merge['total_buy_vol'] = merge[['vn_retail_buy_vol', 'fr_retail_buy_vol', 'vn_institute_buy_vol', 'fr_institute_buy_vol']].sum(axis=1)
merge['vol_log'] = np.log(merge['total_buy_vol'])
merge['vol_spread'] = merge['vol_log'] - np.log(total_outstanding_share) 
merge['z_score_vol'] = ((merge['vol_spread'] - merge['vol_spread'].mean()) / merge['vol_spread'].std())
merge['vol_ratio'] = merge['total_buy_vol'] / total_market_cap

merge.drop(columns=['vn_retail_buy_vol', 'vn_retail_buy_value', 'vn_retail_sell_vol',
       'vn_retail_sell_value', 'fr_retail_buy_vol', 'fr_retail_buy_value',
       'fr_retail_sell_vol', 'fr_retail_sell_value', 'vn_institute_buy_vol',
       'vn_institute_buy_value', 'vn_institute_sell_vol',
       'vn_institute_sell_value', 'fr_institute_buy_vol',
       'fr_institute_buy_value', 'fr_institute_sell_vol',
       'fr_institute_sell_value', 'total_buy_vol', 'vol_spread'], inplace=True)
mean_val = merge['z_score_vol'].mean()
latest_vol = merge['z_score_vol'].iloc[-1]

""" Calculate bouncing power """
_, _, vol_mean = calculate_threshold(merge['z_score_vol'])
vol_min = -2
vol_max = 2.5
if latest_vol <= vol_min:
    losing_percentage = 0
elif vol_max > latest_vol > vol_min:
    losing_percentage = percentage_position(latest_vol, vol_min, vol_max)
elif latest_vol >= vol_max:
    losing_percentage = 100

# print(f"⁜⁜⁜ Losing percentage: {losing_percentage:.2f}% ⁜⁜⁜")

if losing_percentage > 50:
    bouncing_power = losing_percentage
    power_index = f"⁜ GOING DOWN PROBABILITY: {bouncing_power:.2f}%"
else:
    bouncing_power = 100 - losing_percentage
    power_index = f"⁜ GOING UP PROBABILITY: {bouncing_power:.2f}% "

""" Calculate risk """
risk_min, risk_max, risk_mean = calculate_threshold(merge['z_score_vol'])

if latest_vol <= risk_min:
    risk = 0
elif risk_max > latest_vol > risk_min:
    risk = percentage_position(latest_vol, risk_min, risk_max)
elif latest_vol >= risk_max:
    risk = 100

risk_index = f"⁜⁜ RISK LEVEL: {risk:.2f}%"
# zoom_in = merge#.loc["2024-01-01":]