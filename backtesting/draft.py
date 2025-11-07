import pandas as pd

path = "vnindex_strategy.csv"

df = pd.read_csv(path)
df["time"] = pd.to_datetime(df["time"])

# List of target dates in DD/MM/YYYY format
target_dates = [
    "31/12/2021", "12/01/2022", "28/01/2022", "28/02/2022", "31/03/2022", "29/04/2022",
    "16/05/2022", "31/05/2022", "30/06/2022", "29/07/2022", "30/08/2022", "30/09/2022",
    "31/10/2022", "30/11/2022", "30/12/2022", "31/01/2023", "31/03/2023", "30/06/2023",
    "31/08/2023", "29/09/2023", "29/12/2023", "29/03/2024", "26/04/2024", "28/06/2024",
    "30/09/2024", "31/12/2024", "31/03/2025", "30/06/2025", "30/09/2025"
]

# Convert to datetime
target_dates = pd.to_datetime(target_dates, format="%d/%m/%Y")

# Make sure df is sorted by time
df = df.sort_values("time")

# Find nearest available date for each target
results = []
for date in target_dates:
    # get index of nearest available date
    idx = df["time"].sub(date).abs().idxmin()
    row = df.loc[idx, ["time", "asset_allocation"]]
    results.append(row)

# Convert to a clean output DataFrame
out = pd.DataFrame(results).reset_index(drop=True)
print(out)
print(df)