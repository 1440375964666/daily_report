import index_constructor
import numpy as np
from datetime import date
import pandas as pd
import sys
import os

# === Load the data ===
path = "all_indices.csv"
indices = pd.read_csv(path)
indices.set_index('time', inplace=True)

tomorrow_str = (date.today() + pd.Timedelta(days=1)).strftime("%Y-%m-%d")

# === Step 1: Define which columns to log (exclude 'index') ===
cols_to_log = [col for col in indices.columns if col != 'index']

# === Step 2: Apply log transformation ===
log_indices = indices.copy()
log_indices[cols_to_log] = np.log(indices[cols_to_log])
log_indices['index'] = np.log(indices['index'])  # optional, keeps scale consistent

# === Step 3: Subtract index column to compute spread ===
spread_df = log_indices[cols_to_log].subtract(log_indices['index'], axis=0)

# === Step 4: Calculate z-score for each column ===
z_score_df = (spread_df - spread_df.mean()) / spread_df.std()

# === Step 5: Get the latest row (last date) ===
last_row = z_score_df.iloc[-1]

# === Step 6: Rank columns by descending value ===
ranked = last_row.sort_values(ascending=False)

# === Step 7: Calculate relative weights based on last 5 (lowest) z-scores ===
sum_abs = abs(ranked[-5:]).sum()
weight = (abs(ranked) / sum_abs) * 100
current_weight = weight[-5:]
# print(weight)
message = "**📊 Sector Weighting Update**\n\n"
message += f"**Date:** {tomorrow_str}\n\n"
for sector, value in current_weight.items():
    message += f"- **{sector}**: {value:.2f}%\n"
    
# # === Optional: Export ===
# print(message)

# === Save the message to a file ===
output_path = "../sector_weighting_update.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(message)

print(f"✅ Sector weighting update saved to {output_path}")
