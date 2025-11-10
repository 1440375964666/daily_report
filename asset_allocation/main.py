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
OUT_W = 800       # pixels wide
OUT_H = 500        # pixels high
DPI = 100
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

# print(kelly)
today_str = date.today().strftime("%Y-%m-%d")
today_formatted = date.today().strftime("%Y_%m_%d")
# tomorrow_str = (date.today() + pd.Timedelta(days=1)).strftime("%Y_%m_%d")

# Table data
table_data = [
    [asset_allocation]
]
column_header = [f"Khuyến nghị tự doanh: {today_formatted}"]
# print(regime_changed_date)
# print(merge)
merge.index = pd.to_datetime(merge.index)
merge = merge.loc[merge.index >= pd.Timestamp("2025-01-01")]
# print(df_cut)
# merge = merge.loc["2025-01-01":] #"2025-07-25"

# ================================
# Figure and layout (2 rows: plot + table)
# ================================
fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
gs = GridSpec(2, 1, height_ratios=[4, 1], figure=fig)

ax_plot = fig.add_subplot(gs[0])
ax_table = fig.add_subplot(gs[1])

# --- Plot SELLING PRESSURE ---
ax_plot.plot(merge.index, merge['z_score_vol'], label='Pressure', color='orange', linewidth=1.8)
ax_plot.set_title('SELLING PRESSURE', fontsize=14, fontweight='bold', pad=10)
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
plt.close(fig)

print(f"✅ Saved chart: {out_path} (expected {OUT_W}×{OUT_H} px)")

# Verify with Pillow
try:
    im = Image.open(out_path)
    print("Actual image size (px):", im.size)
except Exception as e:
    print("⚠️ Unable to verify image size:", e)
