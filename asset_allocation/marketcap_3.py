# import pandas as pd

# # path_hp = 'historical_price.csv'
# # historical_price = pd.read_csv(path_hp)
# # historical_price.drop([ 'timestamp', 'open', 'high', 'low', 'volume', 'bu', 'sd'], axis=1, inplace=True)
# # historical_price.set_index('ticker', inplace=True)
# # print(historical_price)

# path_os = 'outstanding_share.csv'
# outstanding_share = pd.read_csv(path_os)
# outstanding_share.sort_values(by=['so_cp_luu_hanh'], ascending=True, inplace=True)
# outstanding_share.set_index('symbol', inplace=True)
# print(outstanding_share)
# # # ====================================================
# # merged_df = pd.merge(historical_price, outstanding_share, left_index=True, right_index=True)
# # merged_df['market_cap'] = merged_df['close'] * merged_df['so_cp_luu_hanh']
# # total_market_cap = merged_df['market_cap'].sum()
# # total_outstanding_share = outstanding_share['so_cp_luu_hanh'].sum()

# from vnstock_data import Finance, Quote
# from datetime import date, timedelta

# today = date.today()
# yesterday = date.today() - timedelta(days=1)
# quote = Quote(source='vnd', symbol="VNINDEX")
# vnindex = quote.history(start=f"{yesterday}", end=f"{today}", interval="1D")

import sys
import os
# Add root path to access index_constructor.py
sys.path.append(os.path.abspath("../")) # ../../

import pandas as pd
from vnstock_data import Finance, Quote
import time
import json
from tqdm import tqdm
from datetime import date, timedelta

path = 'top_liquidity_symbols.json'
with open(path, 'r') as f:
    filtered_labels = json.load(f)

# Prepare empty list to collect data
data = []

# Loop through each symbol
for symbol in tqdm(filtered_labels):
    try:
        fin = Finance(symbol=symbol, period='year', source='VCI')  # use symbol as source
        a = fin.ratio(lang='vi')

        # Extract 'Số CP lưu hành (Triệu CP)'
        so_cp_luu_hanh = a['Số CP lưu hành (triệu)'].iloc[-1]
        data.append({'symbol': symbol, 'so_cp_luu_hanh': so_cp_luu_hanh})

    except Exception as e:
        print(f"Error with symbol {symbol}: {e}")
        data.append({'symbol': symbol, 'so_cp_luu_hanh': None})  # or skip if preferred

# Create result DataFrame
outstanding_share = pd.DataFrame(data)

# Drop rows with missing symbol or outstanding shares
outstanding_share.dropna(subset=['symbol', 'so_cp_luu_hanh'], inplace=True)
outstanding_share.sort_values(by=['so_cp_luu_hanh'], ascending=False, inplace=True)

# Limit for testing (you can remove this)
# outstanding_share = outstanding_share.head(10)

# === 2️⃣ Prepare result list ===
results = []

today = date.today()
yesterday = today - timedelta(days=5)  # fetch last few days to ensure data exists

# === 3️⃣ Loop through symbols and fetch close price ===
for symbol in tqdm(outstanding_share['symbol']):
    try:
        quote = Quote(source='vnd', symbol=symbol)
        df = quote.history(start=str(yesterday), end=str(today), interval="1D")
        if not df.empty:
            close_price = df['close'].iloc[-1]
            results.append({
                'symbol': symbol,
                'so_cp_luu_hanh': outstanding_share.loc[outstanding_share['symbol'] == symbol, 'so_cp_luu_hanh'].values[0],
                'close': close_price
            })
        else:
            results.append({
                'symbol': symbol,
                'so_cp_luu_hanh': outstanding_share.loc[outstanding_share['symbol'] == symbol, 'so_cp_luu_hanh'].values[0],
                'close': None
            })
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        results.append({
            'symbol': symbol,
            'so_cp_luu_hanh': outstanding_share.loc[outstanding_share['symbol'] == symbol, 'so_cp_luu_hanh'].values[0],
            'close': None
        })
    time.sleep(0.2)  # small delay to avoid API rate limit

# === 4️⃣ Create final DataFrame ===
final_df = pd.DataFrame(results)
final_df.sort_values(by='so_cp_luu_hanh', ascending=False, inplace=True)
final_df.reset_index(drop=True, inplace=True)

# === 5️⃣ Save & print ===
final_df.to_csv('outstanding_with_close.csv', index=False)
print("\n✅ Saved to outstanding_with_close.csv")
