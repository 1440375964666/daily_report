from asset_allocation.risk_5 import merge
from asset_allocation.kelly_4 import asset_allocation
import matplotlib.pyplot as plt
from datetime import date
from matplotlib.gridspec import GridSpec
import os
from PIL import Image
import pandas as pd

# ================================
# Output configuration
# ================================
OUT_W = 800       # pixels wide
OUT_H = 500        # pixels high
DPI = 100
FIGSIZE = (OUT_W / DPI, OUT_H / DPI)  # inches

# ================================
# Load and prepare data
# ================================
ytd = merge  # optionally filter: .loc["2024-01-01":]
today_str = date.today().strftime("%Y-%m-%d")
today_formatted = date.today().strftime("%Y_%m_%d")
tomorrow_str = (date.today() + pd.Timedelta(days=1)).strftime("%Y_%m_%d")

# Table data
table_data = [
    [asset_allocation]
]
column_header = [f"Khuyến nghị tự doanh: {tomorrow_str}"]

# ================================
# Figure and layout (2 rows: plot + table)
# ================================
fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
gs = GridSpec(2, 1, height_ratios=[4, 1], figure=fig)

ax_plot = fig.add_subplot(gs[0])
ax_table = fig.add_subplot(gs[1])

# --- Plot SELLING PRESSURE ---
ax_plot.plot(ytd.index, ytd['z_score_vol'], label='Pressure', color='orange', linewidth=1.8)
ax_plot.set_title('SELLING PRESSURE', fontsize=14, fontweight='bold', pad=10)
ax_plot.set_ylabel('SCORE')
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
out_path = f"selling_pressure_{tomorrow_str}.png" #os.path.join(out_dir, out_name)

fig.savefig(out_path, dpi=DPI)
plt.close(fig)

print(f"✅ Saved chart: {out_path} (expected {OUT_W}×{OUT_H} px)")

# Verify with Pillow
try:
    im = Image.open(out_path)
    print("Actual image size (px):", im.size)
except Exception as e:
    print("⚠️ Unable to verify image size:", e)
