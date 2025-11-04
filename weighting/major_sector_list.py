import json
from vnstock_data import Company, Listing
import pandas as pd
import requests

with open('../asset_allocation/top_liquidity_symbols.json', 'r') as f: #../../../
    liquidity_list = json.load(f)

listing = Listing(source='vci')
symbol_by_sector = listing.symbols_by_industries()[['symbol', 'icb_name3', 'icb_code3']]

# 1) Unique values of icb_name3 (as a Python list)
unique_icb_names = symbol_by_sector['icb_name3'].drop_duplicates().tolist()

# 2) Map icb_code3 -> icb_name3 (unique)  (nice for JSON)
code_to_name = (
    symbol_by_sector[['icb_code3', 'icb_name3']]
    .drop_duplicates()
    .set_index('icb_code3')['icb_name3']
    .to_dict()
)

# 3) Map icb_code3 -> list of symbols that share that code
symbols_by_code = (
    symbol_by_sector.groupby('icb_code3')['symbol']
      .apply(list)
      .to_dict()
)

# Filter dictionary
filtered_dict = {
    key: [symbol for symbol in symbols if symbol in liquidity_list]
    for key, symbols in symbols_by_code.items()
    if any(symbol in liquidity_list for symbol in symbols)
}

print(f"✅ Loaded {len(liquidity_list)} high-liquidity symbols")