import pandas as pd
from datetime import date
from vnstock_data import Trading, Listing, Quote
from regime.checker import regime_changed_date
import json
from tqdm import tqdm

symbol_list = Listing(source="VND").all_symbols()

filtered_df = symbol_list[
    (symbol_list['exchange'].isin(['HOSE', 'HNX', 'UPCOM'])) &
    (symbol_list['status'] == 'listed') &
    (symbol_list['type'] == 'STOCK')
]

# Extract symbol list
all_symbols = sorted(filtered_df['symbol'].drop_duplicates().tolist())

min_daily_volume = 0
# Create an empty DataFrame to store matched_value for all symbols
matched_value_df = pd.DataFrame()
# Get today's date
first_day = regime_changed_date
last_day = date.today()

# Loop through symbols and collect matched_value
for symbol in tqdm(all_symbols):
    try:
        quote = Quote(source="mas", symbol=symbol)
        df = quote.history(start=f"{first_day}", end=f'{last_day}', interval="1D")

        # Convert index to datetime if needed
        df['time'] = pd.to_datetime(df['time'])
        df['adjusted_price'] = df['close'] * 1000

        # Remove today's row if it exists
        df = df[df['time'] < pd.Timestamp(last_day)]
        df["matched_value"] = df["volume"] * df["adjusted_price"]

        if not df.empty and "matched_value" in df.columns:
            temp = df[["matched_value"]].copy()
            temp.rename(columns={"matched_value": symbol}, inplace=True)

            # Merge with main df
            if matched_value_df.empty:
                matched_value_df = temp
            else:
                matched_value_df = matched_value_df.join(temp, how='outer')

    except Exception as e:
        print(f"Error processing {symbol}: {e}")

daily_avg_volume = matched_value_df.mean()
filtered_labels = daily_avg_volume[daily_avg_volume > min_daily_volume].index.to_list()
# print(f"Filtered symbols count: {len(filtered_labels)}")

with open('top_liquidity_symbols.json', 'w') as f:
    json.dump(filtered_labels, f)
