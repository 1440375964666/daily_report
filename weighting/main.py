import sys
import os
# Add root path to access index_constructor.py
sys.path.append(os.path.abspath("../../../"))

import index_constructor
import pandas as pd
import matplotlib.pyplot as plt
from func_ranking import ranked
import matplotlib.dates as mdates
import numpy as np
from major_sector_list import code_to_name, filtered_dict
from xlsxwriter import Workbook
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
# print(ranked)
# print(code_to_name)
# print(filtered_dict)

# Create DataFrame for overvalued sectors
overvalued_df = ranked[ranked > 0].sort_values(ascending=False).reset_index()
overvalued_df.columns = ['Sector', 'Z-Score']
overvalued_df['Rank'] = overvalued_df['Z-Score'].rank(ascending=False).astype(int)
# Create DataFrame for undervalued sectors
undervalued_df = ranked[ranked < 0].sort_values(ascending=True).reset_index()
undervalued_df.columns = ['Sector', 'Z-Score']
undervalued_df['Rank'] = undervalued_df['Z-Score'].rank(ascending=True).astype(int)
# 3. Sector-Symbol table
sector_symbols = {
    code_to_name[code]: symbols
    for code, symbols in filtered_dict.items()
    if code in code_to_name
}
df_sector_symbols = pd.DataFrame(list(sector_symbols.items()), columns=["Sector", "Symbols"])
df_sector_symbols["Symbols"] = df_sector_symbols["Symbols"].apply(lambda x: ", ".join(x))

# overvalued_df.set_index("Sector", inplace=True)
# undervalued_df.set_index("Sector", inplace=True)
# df_sector_symbols.set_index("Sector", inplace=True)

# Save to one Excel file with different sheets
with pd.ExcelWriter(f"sector_ranking_{today}.xlsx", engine="xlsxwriter") as writer:
    overvalued_df.to_excel(writer, sheet_name="overvalued", index=False)
    undervalued_df.to_excel(writer, sheet_name="undervalued", index=False)
    df_sector_symbols.to_excel(writer, sheet_name="sector_symbols", index=False)



