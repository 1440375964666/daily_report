from vnstock_data import Listing
import pandas as pd
import json

symbol_list = Listing(source="VND").all_symbols()

filtered_df = symbol_list[
    (symbol_list['exchange'].isin(['HOSE', 'HNX', 'UPCOM'])) &
    (symbol_list['status'] == 'listed') &
    (symbol_list['type'] == 'STOCK')
]

# Extract symbol list
all_symbols = sorted(filtered_df['symbol'].drop_duplicates().tolist())
print(all_symbols)
# with open('data/calculated/all_symbols_vnd.json', 'w') as f:
#     json.dump(all_symbols, f)
