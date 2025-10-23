from risk import losing_percentage, risk, merge
from regime.checker import regime_changed_date
import matplotlib.pyplot as plt
from datetime import date
from matplotlib.gridspec import GridSpec
import os
from PIL import Image
import pandas as pd
from vnstock_data import Quote

# ================================
# Output configuration
# ================================
OUT_W = 870       # pixels wide
OUT_H = 372        # pixels high
DPI = 88
FIGSIZE = (OUT_W / DPI, OUT_H / DPI)  # inches

losing_percentage = risk / 100
winning_percentage = (100 - risk) / 100
net_odd = 4.336129

def kelly_fraction(winning_probability, net_odd):
    """
    p: Probability of winning
    b: Net odds (b to 1, e.g., 1 if you double your money)
    """
    return (winning_probability * net_odd - losing_percentage) / net_odd

kelly = kelly_fraction(winning_percentage, net_odd) * 100

if kelly < 0:
    asset_allocation = (
        f"⁜⁜⁜ KELLY CRITERION ASSET ALLOCATION: "
        f"Short {abs(kelly):.2f}% VN30 || Hold 0% stocks || Hold {100 - abs(kelly):.2f}% cash"
    )
else:
    asset_allocation = (
        f"⁜⁜⁜ KELLY CRITERION ASSET ALLOCATION: "
        f"Short 0% VN30 || Hold {kelly:.2f}% stocks || Hold {100 - kelly:.2f}% cash"
    )

# path = "../clean_data/trading_data.csv"

# sell_spread = pd.read_csv(path)
# sell_spread['date'] = pd.to_datetime(sell_spread['date']).dt.date
# sell_spread.sort_values(by='date', inplace=True)
# sell_spread.dropna(inplace=True)

# """ Refine VNI data """
# first_day = sell_spread['date'].iloc[0]
# last_day = sell_spread['date'].iloc[-1]
# quote = Quote(source='vnd', symbol="VNINDEX")
# vnindex = quote.history(start=f"{first_day}", end=f"{last_day}", interval="1D")
# vnindex = vnindex[["time", "close"]]
# vnindex['time'] = pd.to_datetime(vnindex['time']).dt.date
# vnindex = vnindex.rename(columns={"close": "vnindex", "time": "date"})

# """ Total market cap & outstanding share """
# path = 'outstanding_with_close.csv'
# outstanding_share = pd.read_csv(path)
# outstanding_share['market_cap'] = outstanding_share['close'] * outstanding_share['so_cp_luu_hanh']
# total_market_cap = outstanding_share['market_cap'].sum()
# total_outstanding_share = outstanding_share['so_cp_luu_hanh'].sum()

# """ Merge & calculate """
# merge = pd.merge(sell_spread, vnindex, on='date')
# merge.set_index('date', inplace=True)
# merge = merge.loc[regime_changed_date] #"2025-07-25"
# print(merge)

# ytd = merge  # optionally filter: .loc["2024-01-01":]
today_str = date.today().strftime("%Y-%m-%d")
today_formatted = date.today().strftime("%Y_%m_%d")
# tomorrow_str = (date.today() + pd.Timedelta(days=1)).strftime("%Y_%m_%d")

# Table data
table_data = [
    [asset_allocation]
]
column_header = [f"Khuyến nghị tự doanh: {today_formatted}"]

# ================================
# Figure and layout (2 rows: plot + table)
# ================================
fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
gs = GridSpec(2, 1, height_ratios=[4, 1], figure=fig)

ax_plot = fig.add_subplot(gs[0])
ax_table = fig.add_subplot(gs[1])

# --- Plot SELLING PRESSURE ---
ax_plot.plot(merge.index, merge['z_score_vol'], label='Pressure', color='orange', linewidth=1.8)
ax_plot.set_title('SELLING PRESSURE', fontsize=11, fontweight='bold', pad=8)
# ax_plot.set_ylabel('SCORE')
ax_plot.grid(True, alpha=0.3)
ax_plot.legend(loc='upper left', fontsize=9)

# --- Add TABLE ---
ax_table.axis('off')
table = ax_table.table(
    cellText=table_data,
    colLabels=column_header,
    loc='center',
    cellLoc='left'
)
table.scale(1, 2.2)

# Adjust layout (ensure no cut-off at fixed size)
plt.subplots_adjust(left=0.07, right=0.97, top=0.93, bottom=0.05, hspace=0.25)

# ================================
# Save exactly at OUT_W × OUT_H pixels
# ================================
# out_dir = "/"
# out_name = f"selling_pressure_{OUT_W}x{OUT_H}.png"
out_path = f"../selling_pressure_{today_formatted}.png" #os.path.join(out_dir, out_name)

fig.savefig(out_path, dpi=DPI)
# plt.close(fig)

print(f"✅ Saved chart: {out_path} (expected {OUT_W}×{OUT_H} px)")

# Verify with Pillow
try:
    im = Image.open(out_path)
    print("Actual image size (px):", im.size)
except Exception as e:
    print("⚠️ Unable to verify image size:", e)
