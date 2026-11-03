import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# Set matplotlib fonts
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 1. Load daily data
df_daily = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/daily_stocks_vs_etfs_tech_margin.csv')
df_daily = df_daily[df_daily['date'] >= 20260922].copy()
df_daily['date_dt'] = pd.to_datetime(df_daily['date'].astype(str))
df_daily = df_daily[df_daily['stock_count'] == 15].copy() # keep comparable days

# 2. Load category stats
df_cat = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/etf_category_margin_stats.csv')

# 3. Load stock stats
df_stocks = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/tech_stocks_margin_stats.csv')

fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=150)

# --- Subplot 1: Total Margin Balance (Absolute Value) ---
ax1 = axes[0, 0]
ax1_twin = ax1.twinx()

line1 = ax1.plot(df_daily['date_dt'], df_daily['stock_total_margin_yi'], color='#d62728', linewidth=2.5, marker='o', label='15大科技权重个股总融资额(左轴)')
line2 = ax1_twin.plot(df_daily['date_dt'], df_daily['etf_broad_margin_yi'], color='#1f77b4', linewidth=2.5, marker='s', label='双创宽基ETF总融资额(右轴)')
line3 = ax1_twin.plot(df_daily['date_dt'], df_daily['etf_total_margin_yi'], color='#2ca02c', linewidth=2.0, linestyle='--', marker='^', label='科技全类别ETF总融资额(右轴)')

ax1.set_title('图1：科技权重个股总融资额 vs 双创/科技ETF总融资额走势 (绝对金额)', fontsize=13, fontweight='bold', pad=10)
ax1.set_ylabel('15大科技个股融资总额 (亿元)', color='#d62728', fontsize=11)
ax1_twin.set_ylabel('科技ETF融资总额 (亿元)', color='#1f77b4', fontsize=11)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

# Combine legends
lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center left', framealpha=0.8)

# Annotate start and end
ax1.annotate(f"{df_daily.iloc[0]['stock_total_margin_yi']:.1f}亿", 
             (df_daily.iloc[0]['date_dt'], df_daily.iloc[0]['stock_total_margin_yi']),
             textcoords="offset points", xytext=(-10, 10), ha='center', color='#d62728', fontweight='bold')
ax1.annotate(f"{df_daily.iloc[-1]['stock_total_margin_yi']:.1f}亿\n(净流出 -380亿)", 
             (df_daily.iloc[-1]['date_dt'], df_daily.iloc[-1]['stock_total_margin_yi']),
             textcoords="offset points", xytext=(-20, -25), ha='center', color='#d62728', fontweight='bold')

ax1_twin.annotate(f"{df_daily.iloc[0]['etf_broad_margin_yi']:.1f}亿", 
                  (df_daily.iloc[0]['date_dt'], df_daily.iloc[0]['etf_broad_margin_yi']),
                  textcoords="offset points", xytext=(10, -15), ha='center', color='#1f77b4', fontweight='bold')
ax1_twin.annotate(f"{df_daily.iloc[-1]['etf_broad_margin_yi']:.1f}亿\n(净流入 +58亿)", 
                  (df_daily.iloc[-1]['date_dt'], df_daily.iloc[-1]['etf_broad_margin_yi']),
                  textcoords="offset points", xytext=(10, 10), ha='center', color='#1f77b4', fontweight='bold')

# --- Subplot 2: Relative Cumulative Change (%) Normalized to 2026-09-22 ---
ax2 = axes[0, 1]
norm_stock = (df_daily['stock_total_margin_yi'] / df_daily['stock_total_margin_yi'].iloc[0] - 1.0) * 100
norm_etf_broad = (df_daily['etf_broad_margin_yi'] / df_daily['etf_broad_margin_yi'].iloc[0] - 1.0) * 100
norm_etf_total = (df_daily['etf_total_margin_yi'] / df_daily['etf_total_margin_yi'].iloc[0] - 1.0) * 100

ax2.plot(df_daily['date_dt'], norm_etf_broad, color='#1f77b4', linewidth=2.5, marker='s', label='双创宽基ETF融资变动% (+99.7%)')
ax2.plot(df_daily['date_dt'], norm_etf_total, color='#2ca02c', linewidth=2.0, linestyle='--', marker='^', label='科技全类别ETF融资变动% (+43.5%)')
ax2.plot(df_daily['date_dt'], norm_stock, color='#d62728', linewidth=2.5, marker='o', label='15大科技个股融资变动% (-23.0%)')
ax2.axhline(0, color='black', linestyle='-', linewidth=0.8, alpha=0.7)

ax2.set_title('图2：相对变动速度对比 (基准: 2026-09-22 = 0%)', fontsize=13, fontweight='bold', pad=10)
ax2.set_ylabel('累计变动幅度 (%)', fontsize=11)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax2.legend(loc='upper left', framealpha=0.8)

# Highlight divergence
ax2.fill_between(df_daily['date_dt'], norm_stock, norm_etf_broad, color='#1f77b4', alpha=0.1, label='杠杆替代分化剪刀差')

# --- Subplot 3: ETF Category Margin Flow since Oct 20 (Market Drop) ---
ax3 = axes[1, 0]
top_cats = df_cat[~df_cat['category'].isin(['其他行业主题'])].sort_values('chg_from_oct20_pct', ascending=True).tail(10)
colors = ['#d62728' if x < 0 else '#2ca02c' if x > 10 else '#1f77b4' for x in top_cats['chg_from_oct20_pct']]

bars = ax3.barh(top_cats['category'], top_cats['chg_from_oct20_pct'], color=colors, alpha=0.85, edgecolor='black', linewidth=0.5)
ax3.axvline(0, color='black', linestyle='-', linewidth=0.8)
ax3.set_title('图3：10月20日急跌以来 各类ETF融资额变动率 (%)', fontsize=13, fontweight='bold', pad=10)
ax3.set_xlabel('10月20日以来 融资额增减比例 (%)', fontsize=11)
ax3.grid(True, linestyle=':', alpha=0.6, axis='x')

for bar in bars:
    w = bar.get_width()
    ha = 'left' if w >= 0 else 'right'
    offset = 0.5 if w >= 0 else -0.5
    ax3.text(w + offset, bar.get_y() + bar.get_height()/2, f"{w:+.1f}%", va='center', ha=ha, fontsize=9, fontweight='bold')

# --- Subplot 4: Top Tech Stocks Margin Drop from Peak ---
ax4 = axes[1, 1]
top_stocks_drop = df_stocks.sort_values('drop_from_peak_pct', ascending=True).head(10)
stock_labels = [f"{r['name']} ({r['code'][:6]})" for _, r in top_stocks_drop.iterrows()]
bars4 = ax4.barh(stock_labels, top_stocks_drop['drop_from_peak_pct'], color='#d62728', alpha=0.8, edgecolor='black', linewidth=0.5)
ax4.set_title('图4：核心科技个股 融资额距年内高点回撤幅度 (%)', fontsize=13, fontweight='bold', pad=10)
ax4.set_xlabel('峰值去杠杆回撤率 (%)', fontsize=11)
ax4.grid(True, linestyle=':', alpha=0.6, axis='x')

for bar, (_, r) in zip(bars4, top_stocks_drop.iterrows()):
    w = bar.get_width()
    ax4.text(w - 0.8, bar.get_y() + bar.get_height()/2, f"{w:.1f}% (-{abs(r['abs_drop_from_peak_yi']):.1f}亿)", 
             va='center', ha='right', fontsize=9, fontweight='bold', color='white')

plt.tight_layout()
out_fig = r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/chart6_stocks_vs_etfs_margin_flow.png'
plt.savefig(out_fig)
plt.close()
print(f"Figure saved successfully to: {out_fig}")
