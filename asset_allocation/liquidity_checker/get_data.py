import json
import time
from pathlib import Path
from tqdm import tqdm

import pandas as pd
from vnstock import Company, Quote

# --------- Config ---------
START = "2025-07-03"
END   = "2025-12-31"
INTERVAL = "1D"
JSON_PATH = Path("../top_liquidity_symbols.json")
PAUSE_SEC = 1  # small pause to be gentle with APIs

# --------- Helpers ---------
def get_outstanding_shares(symbol: str) -> float | None:
    """
    Fetch outstanding shares from Company(...).overview().
    Handles a few possible column name variants and returns a float (or None).
    """
    try:
        ov = Company(symbol=symbol, source="TCBS").overview()
        # Normalize columns to lowercase for resilient access
        cols_lower = {c.lower(): c for c in ov.columns}
        # Common variants seen in different vnstock builds
        candidates = [
            "outstanding_share",     # typical
            "outstandingshare",      # no underscore
            "outstanding_shares",    # plural
            "outstanding shares",    # space
            "so_luong_cp_luu_hanh",  # Vietnamese (if present)
        ]
        for key in candidates:
            if key in cols_lower:
                val = ov[cols_lower[key]].iloc[0]
                return pd.to_numeric(val, errors="coerce")
        return None
    except Exception as e:
        # Print once for diagnostics, but don't fail the loop
        print(f"[WARN] {symbol}: get_outstanding_shares failed: {e}")
        return None

def get_mean_volume(symbol: str, start: str, end: str, interval: str) -> float | None:
    """
    Fetch historical bars and return mean of 'volume' over the period.
    """
    try:
        q = Quote(symbol=symbol, source="mas")
        df = q.history(start=start, end=end, interval=interval)
        if df is None or df.empty:
            return None
        # Coerce to numeric in case volume is string-typed
        vol = pd.to_numeric(df["volume"], errors="coerce")
        # Drop NaNs before mean
        vol = vol.dropna()
        return float(vol.mean()) if not vol.empty else None
    except Exception as e:
        print(f"[WARN] {symbol}: get_mean_volume failed: {e}")
        return None

# --------- Main ---------
def build_liquidity_df(symbols: list[str],
                       start: str = START,
                       end: str = END,
                       interval: str = INTERVAL) -> pd.DataFrame:
    rows = []
    for i, sym in enumerate(tqdm(symbols, desc="Processing symbols"), 1):
        sym = sym.strip().upper()
        mean_vol = get_mean_volume(sym, start, end, interval)
        out_shares = get_outstanding_shares(sym)
        rows.append(
            {
                "symbol": sym,
                "mean_volume": mean_vol,
                "outstanding_shares": out_shares,
            }
        )
        # Light throttling
        time.sleep(PAUSE_SEC)
        # if i % 20 == 0:
        #     print(f"...processed {i} symbols")

    df = pd.DataFrame(rows)
    # Optional: sort by mean_volume descending
    df = df.sort_values(by=["mean_volume"], ascending=False, na_position="last").reset_index(drop=True)
    return df

# --------- Load symbols and run ---------
with open(JSON_PATH, "r", encoding="utf-8") as f:
    symbols = json.load(f)

result_df = build_liquidity_df(symbols, START, END, INTERVAL)

# # Display summary
# print(result_df.head(20))

# Optional: save to CSV
out_file = Path("mean_volume_outstanding_shares.csv")
result_df.to_csv(out_file, index=False, encoding="utf-8-sig")
print(f"Saved to {out_file.resolve()}")
