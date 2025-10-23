import matplotlib.pyplot as plt
import ruptures as rpt
from vnstock_data import Quote
from datetime import date
import numpy as np
import math
import pandas as pd

# -------------------------
# Output target (pixels)
# -------------------------
OUT_W = 800
OUT_H = 350
DPI = 100  # choose DPI such that OUT_W/DPI and OUT_H/DPI are reasonable
FIGSIZE = (OUT_W / DPI, OUT_H / DPI)  # inches

# -------------------------
# Fetch data
# -------------------------
today = date.today()
today_formatted = date.today().strftime("%Y_%m_%d")
# tomorrow_str = (date.today() + pd.Timedelta(days=1)).strftime("%Y_%m_%d")
quote = Quote(source='vnd', symbol="VNINDEX")
df = quote.history(start="2000-01-01", end=f"{today}", interval="1D")
df = df[["time", "volume"]]
df.set_index("time", inplace=True)

# Protect against zeros/negatives before taking log
vol = df["volume"].replace(0, np.nan).dropna()
if vol.empty:
    raise ValueError("Volume series is empty after removing zeros/NaNs.")

signal = vol.values
log_signal = np.log(signal)

# -------------------------
# Change point detection
# -------------------------
model = "l2"  # mean shift
algo = rpt.Pelt(model=model).fit(log_signal)
breakpoints = algo.predict(pen=10)

# Pick last detected breakpoint (skip final len(signal) breakpoint)
if len(breakpoints) > 1:
    bp_index = breakpoints[-2]  # second-last breakpoint index (last is len(signal))
    bp_date = vol.index[bp_index]
    regime_changed_date = bp_date.date()
    print(f"Checkpoint date: {regime_changed_date}")
else:
    bp_date = None
    print("No breakpoints (other than final) found.")

# -------------------------
# Plot and save EXACT pixel size
# -------------------------
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

# Plot whole series (aligning index)
# Note: use vol (which may be shorter than df if zeros were removed). If you want original df, revert to df["volume"]
ax.plot(vol.index, vol.values, label="Volume")

# Add breakpoints as vertical lines (skip final len(signal))
for bp in breakpoints[:-1]:
    # skip if bp equals len(signal) (ruptures often appends final index)
    if bp >= len(vol):
        continue
    bp_date_local = vol.index[bp]
    ax.axvline(x=bp_date_local, color="red", linestyle="--",
               linewidth=1, label=f"Breakpoint: {bp_date_local.date()}")

# Avoid duplicate legend labels
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize="small")

# Formatting
ax.set_title("Trạng thái thanh khoản VNINDEX")
# ax.set_xlabel("Date")
ax.set_ylabel("Volume")
ax.grid(True)

# Make sure layout fits within the fixed figure size without using bbox_inches='tight'
plt.subplots_adjust(left=0.07, right=0.98, top=0.92, bottom=0.12)

# Save exactly at OUT_W x OUT_H pixels
out_path = f"vnindex_volume_{today_formatted}.png"
fig.savefig(out_path, dpi=DPI)  # figsize * dpi -> EXACT pixel dimensions
plt.close(fig)

print(f"Saved: {out_path} (expected {today_formatted} px)")
# Optional verification (Pillow)
try:
    from PIL import Image
    im = Image.open(out_path)
    print("Resulting image size (px):", im.size)
except Exception:
    pass
