
# import numpy as np
# import pandas as pd

# # Load the data
# path = "all_indices.csv"
# indices = pd.read_csv(path)
# indices.set_index('time', inplace=True)

# # Set columns to divide
# cols_to_divide = [col for col in indices.columns if col not in ['index']]

# # Perform division
# spread_df = indices[cols_to_divide].subtract(indices['index'], axis=0)

# # Calculate z-score for each column
# z_score_df = (spread_df - spread_df.mean()) / spread_df.std()

# # Step 1: Get the last row (excluding the 'time' column)
# last_row = z_score_df.iloc[-1]  # all columns except 'time'

# # Step 2: Sort columns by value descending
# ranked = last_row.sort_values(ascending=False)

# sum_abs = abs(ranked[-5:]).sum()

# weight = (abs(ranked) / sum_abs) * 100

# current_weight = weight[-5:]

# # z_score_df.to_csv("z_score_spread.csv")
# print(current_weight)
# print(indices)

from weighting import index_constructor
import numpy as np
import pandas as pd

# === Load the data ===
path = "all_indices.csv"
indices = pd.read_csv(path)
indices.set_index('time', inplace=True)

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

message = "**📊 Sector Weighting Update**\n\n"
message += f"**Date:** {current_weight.name}\n\n"
for sector, value in current_weight.items():
    message += f"- **{sector}**: {value:.2f}%\n"
# === Optional: Export ===
# z_score_df.to_csv("z_score_spread.csv")

# === Output ===
# print(ranked)
# print(z_score_df)
print(message)
