import pandas as pd
from vnstock_data import Finance, Quote
import time
import json
from tqdm import tqdm
from datetime import date, timedelta
import liquidity_filter as liquidity_filter

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
