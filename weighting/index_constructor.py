from weighting import major_sector_list
from vnstock_data import Trading, Quote
import pandas as pd
from datetime import date, timedelta
from tqdm import tqdm
import time

today = date.today() 
start_date = "2025-07-03"

def calculate_allshare_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate an index using the formula: sum(prices) / number of stocks per row.
    
    Parameters:
    - df: DataFrame with a 'time' column and one or more stock price columns.
    
    Returns:
    - A DataFrame with 'time' and 'index' columns.
    """
    if 'time' not in df.columns:
        raise ValueError("The DataFrame must contain a 'time' column.")
    
    # Extract price columns (exclude 'time')
    price_data = df.drop(columns=['time'])
    
    # Calculate index
    index_values = price_data.sum(axis=1)
    
    # Return new DataFrame with index
    return pd.DataFrame({
        'time': df['time'],
        'index': index_values
    })
def get_allshare_index(symbols: list[str], start_date: str = {start_date}) -> pd.DataFrame:
    sector_df = None

    for symbol in tqdm(symbols, desc="Loading VN_allshare_index"):
        print(f"Loading {symbol}")
        quote = Quote(source='vnd', symbol=symbol)
        df = quote.history(start=start_date, end = f"{today}", interval="1D")

        if df is None or df.empty:
            raise ValueError(f"No data found for symbol: {symbol}")

        df = df[["time","close"]].copy()
        df.rename(columns={"close": symbol}, inplace=True)
        
        if sector_df is None:
            sector_df = df
        else:
            sector_df = pd.merge(sector_df, df, on="time", how="outer")
        time.sleep(0.22)  # To avoid hitting API rate limits

    if sector_df is not None:

        sector_df.sort_values("time", inplace=True)
        sector_df.reset_index(drop=True, inplace=True)

        return calculate_allshare_index(sector_df)
    return pd.DataFrame()  # Empty if no data



def get_sector_index(symbols: dict, start_date: str = start_date) -> pd.DataFrame:
    sector_index_df = None  # Final DataFrame to hold all sector indices

    for code, symbol_list in symbols.items():
        sector_df = None  # Temp DataFrame to build per-sector

        for ticker in tqdm(symbol_list, desc=f"Loading {code}"):
            print(f"Loading {ticker}")
            quote = Quote(source='vnd', symbol=ticker)
            df = quote.history(start=start_date, end=f"{today}", interval="1D")

            if df is None or df.empty:
                print(f"⚠️ No data for {ticker}")
                continue

            df = df[["time", "close"]].copy()
            df.rename(columns={"close": ticker}, inplace=True)

            if sector_df is None:
                sector_df = df
            else:
                sector_df = pd.merge(sector_df, df, on="time", how="outer")

        if sector_df is not None:
            sector_df.sort_values("time", inplace=True)
            sector_df.reset_index(drop=True, inplace=True)

            index_df = calculate_allshare_index(sector_df)
            index_df.rename(columns={"index": code}, inplace=True)

            if sector_index_df is None:
                sector_index_df = index_df
            else:
                sector_index_df = pd.merge(sector_index_df, index_df, on="time", how="outer")

    return sector_index_df

vn_all_index = get_allshare_index(major_sector_list.liquidity_list, start_date=start_date)
sector_index = get_sector_index(major_sector_list.filtered_dict, start_date=start_date)
sector_index.rename(columns={col: major_sector_list.code_to_name[col] for col in sector_index.columns if col in major_sector_list.code_to_name}, inplace=True)

full_index = pd.merge(vn_all_index, sector_index, on="time", how="outer")
full_index.set_index("time", inplace=True)
full_index.to_csv("all_indices.csv")


