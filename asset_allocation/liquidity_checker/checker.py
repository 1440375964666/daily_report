import pandas as pd

def liquidity_checker(symbol, df):
    # Compute global mean vol_ratio
    vol_ratio_mean = df["vol_ratio"].mean()

    if symbol in df["symbol"].values:
        vol_ratio = df[df["symbol"] == symbol]["vol_ratio"].values[0]
        if vol_ratio > vol_ratio_mean:
            print(f"{symbol} Passed liquidity check")
        else:
            print(f"{symbol} Failed liquidity check")
    else:
        print(f"Should not trade {symbol}")


while True:
    symbol = input("Please enter symbol: ").upper()

    path = "mean_volume_outstanding_shares.csv"
    df = pd.read_csv(path)
    df["outstanding_shares"] = df["outstanding_shares"] * 1000000
    df["vol_ratio"] = df["mean_volume"] / df["outstanding_shares"]

    liquidity_checker(symbol, df)