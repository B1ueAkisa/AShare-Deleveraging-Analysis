import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os

# Font configuration
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

output_dir = r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析'
os.makedirs(output_dir, exist_ok=True)

# Load two waves comparison table
df_waves = pd.read_csv(os.path.join(output_dir, 'two_waves_comparison.csv'))

# Load merged data for normalized wave overlay
df_market = pd.read_csv(os.path.join(output_dir, 'merged_market_data.csv'))
df_market['kline_time'] = pd.to_datetime(df_market['kline_time'])

w1_df = df_market[(df_market['kline_time'] >= '2026-06-25') & (df_market['kline_time'] <= '2026-07-31')].copy().reset_index(drop=True)
w2_df = df_market[(df_market['kline_time'] >= '2026-09-22') & (df_market['kline_time'] <= '2026-10-30')].copy().reset_index(drop=True)

# Normalize to 100 at start of wave
for col in ['chinext_close', 'star50_close', 'comm_etf_close', 'chip_etf_close']:
    w1_df[f'{col}_norm'] = w1_df[col] / w1_df[col].iloc[0] * 100
    w2_df[f'{col}_norm'] = w2_df[col] / w2_df[col].iloc[0] * 100

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Panel 1: Normalized Drawdown Comparison (Trading Days elapsed)
ax_p1 = axes[0]
ax_p1.plot(w1_df.index, w1_df['chinext_close_norm'], label='第一波(7月): 创业板指', color='#1f77b4', lw=2, linestyle='--')
ax_p1.plot(w1_df.index, w1_df['star50_close_norm'], label='第一波(7月): 科创50', color='#ff7f0e', lw=2, linestyle='--')
ax_p1.plot(w2_df.index, w2_df['chinext_close_norm'], label='第二波(10月): 创业板指 (-29.0%)', color='#003f5c', lw=2.5)
ax_p1.plot(w2_df.index, w2_df['star50_close_norm'], label='第二波(10月): 科创50 (-30.3%)', color='#d45087', lw=2.5)
ax_p1.plot(w2_df.index, w2_df['comm_etf_close_norm'], label='第二波(10月): 通信ETF (-38.9%)', color='#2f4b7c', lw=1.8, linestyle='-.')
ax_p1.plot(w2_df.index, w2_df['chip_etf_close_norm'], label='第二波(10月): 科创芯片ETF (-34.9%)', color='#f95d6a', lw=1.8, linestyle='-.')

ax_p1.set_xlabel('波段经历交易日数 (天)', fontsize=11, fontweight='bold')
ax_p1.set_ylabel('基准化点位 (波段起点=100)', fontsize=11, fontweight='bold')
ax_p1.set_title('第一波(7月) vs 第二波(10月) 走势轨迹重叠对比', fontsize=13, fontweight='bold')
ax_p1.grid(True, linestyle='--', alpha=0.5)
ax_p1.legend(loc='lower left', fontsize=8.5, framealpha=0.9)

# Panel 2: Deleveraging vs Drawdown Scissors Gap
ax_p2 = axes[1]
waves_labels = ['第一波 (7月出清波)', '第二波 (10月收紧波)']
index_drops = [23.51, 29.01] # ChiNext
margin_drops = [13.99, 10.27] # Total Margin
chip_etf_drops = [75.49, 34.93] # Chip ETF
comm_etf_drops = [69.09, 38.90] # Comm ETF

x = np.arange(len(waves_labels))
width = 0.2

b1 = ax_p2.bar(x - 1.5*width, index_drops, width, label='创业板指跌幅 (%)', color='#003f5c')
b2 = ax_p2.bar(x - 0.5*width, comm_etf_drops, width, label='通信ETF跌幅 (%)', color='#2f4b7c')
b3 = ax_p2.bar(x + 0.5*width, chip_etf_drops, width, label='科创芯片ETF跌幅 (%)', color='#f95d6a')
b4 = ax_p2.bar(x + 1.5*width, margin_drops, width, label='全市场融资去化 (%)', color='#ff7c43')

ax_p2.set_xticks(x)
ax_p2.set_xticklabels(waves_labels, fontsize=11, fontweight='bold')
ax_p2.set_ylabel('变动幅度 (% 绝对值)', fontsize=11, fontweight='bold')
ax_p2.set_title('两波下跌中“股价跌幅 vs 杠杆去化”剪刀差', fontsize=13, fontweight='bold')
ax_p2.grid(True, linestyle='--', alpha=0.5, axis='y')
ax_p2.legend(loc='upper right', fontsize=8.5, framealpha=0.9)

# Add text labels on bars
for bar in b1 + b2 + b3 + b4:
    h = bar.get_height()
    ax_p2.text(bar.get_x() + bar.get_width()/2., h + 1, f'{h:.1f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

# Panel 3: Velocity Comparison (% / day)
ax_p3 = axes[2]
episodes = [
    '第一波: 创业板指 (7月)',
    '第二波: 创业板指 (10月)',
    '第二波: 通信ETF (10月)',
    '第二波: 科创芯片ETF (10月)',
    '10月下旬急跌: 科创50',
    '10月下旬急跌: 科创芯片',
    '2015股灾: 创业板第一波',
    '2020美股: 标普500危机'
]
vels = [0.90, 1.32, 1.77, 1.59, 2.75, 3.19, 1.88, 1.47]
colors = ['#1f77b4', '#003f5c', '#2f4b7c', '#f95d6a', '#d9534f', '#a00000', '#ff7f0e', '#795548']

bars_vel = ax_p3.barh(episodes, vels, color=colors, alpha=0.85, edgecolor='black')
ax_p3.set_xlabel('日均下跌速度 (% / 交易日)', fontsize=11, fontweight='bold')
ax_p3.set_title('第一波 vs 第二波 vs 历史危机：日均跌速排行', fontsize=13, fontweight='bold')
ax_p3.grid(True, linestyle='--', alpha=0.5, axis='x')

for b in bars_vel:
    w = b.get_width()
    ax_p3.text(w + 0.05, b.get_y() + b.get_height()/2, f'{w:.2f}%/日', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'chart4_two_waves_deep_dive.png'), dpi=200)
plt.close(fig)
print("Saved chart4_two_waves_deep_dive.png")
