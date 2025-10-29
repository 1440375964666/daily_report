import pandas as pd

symbol = input("Please enter symbol: ")

path = "mean_volume_outstanding_shares.csv"
df = pd.read_csv(path)
df["outstanding_shares"] = df["outstanding_shares"] * 1000000
df["vol_ratio"] = df["mean_volume"] / df["outstanding_shares"]
vol_ratio_mean = df["vol_ratio"].mean()

# # def liquidity_checker(symbol):
# #     if
# #         return "Pass"
# # print(df)
# import pandas as pd

def liquidity_checker(symbol, df):
    # Compute global mean vol_ratio
    vol_ratio_mean = df["vol_ratio"].mean()

    # Filter for the selected symbol
    row = df[df["symbol"] == symbol.upper()]

    # Check if symbol exists
    if row.empty:
        print(f"Symbol {symbol} not found in dataset.")
        return

    # Extract the vol_ratio of this symbol
    sym_ratio = row["vol_ratio"].iloc[0]

    # Compare
    if sym_ratio > vol_ratio_mean:
        print("Pass")
    else:
        print("Fail")
