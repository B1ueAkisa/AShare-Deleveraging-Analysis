import matplotlib
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

# -------------------------------------------------------------
# Chart 1: 2026双创去杠杆与股价/指数走势（剪刀差与去杠杆弹性）
# -------------------------------------------------------------
df_market = pd.read_csv(os.path.join(output_dir, 'merged_market_data.csv'))
df_market['kline_time'] = pd.to_datetime(df_market['kline_time'])
df_margin = pd.read_csv(os.path.join(output_dir, 'aggregated_margin_summary.csv'))
df_margin['kline_time'] = pd.to_datetime(df_margin['TRADE_DATE'].astype(str))

df_2026 = pd.merge(df_market, df_margin, on='kline_time', how='inner')
df_2026 = df_2026[df_2026['kline_time'] >= '2026-01-01'].copy().sort_values('kline_time').reset_index(drop=True)

fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(14, 10), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# Top plot: ChiNext & STAR 50 & Margin Balance
color_cy = '#1f77b4'
color_star = '#ff7f0e'
color_margin = '#d62728'

ax1.plot(df_2026['kline_time'], df_2026['chinext_close'], label='创业板指 (ChiNext)', color=color_cy, lw=2)
ax1.plot(df_2026['kline_time'], df_2026['star50_close'], label='科创50 (STAR 50)', color=color_star, lw=2)
ax1.set_ylabel('指数点位', fontsize=12, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)

ax2 = ax1.twinx()
ax2.plot(df_2026['kline_time'], df_2026['SUM_BORROW_MONEY_BALANCE'] / 1e12, label='全市场融资余额 (万亿元)', color=color_margin, lw=2.5, linestyle='-.')
ax2.set_ylabel('融资余额 (万亿元)', color=color_margin, fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color_margin)

# Annotate peaks
peak_date_idx = df_2026['SUM_BORROW_MONEY_BALANCE'].idxmax()
peak_date = df_2026.loc[peak_date_idx, 'kline_time']
peak_val = df_2026.loc[peak_date_idx, 'SUM_BORROW_MONEY_BALANCE'] / 1e12
ax2.annotate(f'融资峰值: {peak_val:.3f}万亿\n(2026-06-25)', xy=(peak_date, peak_val),
             xytext=(peak_date - pd.Timedelta(days=50), peak_val * 0.95),
             arrowprops=dict(facecolor=color_margin, shrink=0.05, width=1.5, headwidth=6),
             fontweight='bold', color=color_margin, fontsize=10)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
ax1.set_title('2026年A股双创指数 vs 全市场融资余额（去杠杆剪刀差演变）', fontsize=15, fontweight='bold', pad=15)

# Bottom plot: Normalized Drawdown (%) from 2026-06-25 Peak
peak_cy = df_2026.loc[df_2026['kline_time'] == '2026-06-25', 'chinext_close'].values[0]
peak_star = df_2026.loc[df_2026['kline_time'] == '2026-06-30', 'star50_close'].values[0]
peak_m = df_2026.loc[df_2026['kline_time'] == '2026-06-25', 'SUM_BORROW_MONEY_BALANCE'].values[0]

dd_df = df_2026[df_2026['kline_time'] >= '2026-06-25'].copy()
dd_df['cy_dd'] = (dd_df['chinext_close'] - peak_cy) / peak_cy * 100
dd_df['star_dd'] = (dd_df['star50_close'] - peak_star) / peak_star * 100
dd_df['margin_dd'] = (dd_df['SUM_BORROW_MONEY_BALANCE'] - peak_m) / peak_m * 100

ax3.plot(dd_df['kline_time'], dd_df['cy_dd'], label='创业板指回撤 (-44.79%)', color=color_cy, lw=1.8)
ax3.plot(dd_df['kline_time'], dd_df['star_dd'], label='科创50回撤 (-47.42%)', color=color_star, lw=1.8)
ax3.plot(dd_df['kline_time'], dd_df['margin_dd'], label='融资余额去杠杆幅度 (-21.71%)', color=color_margin, lw=2.5, linestyle='--')
ax3.fill_between(dd_df['kline_time'], dd_df['cy_dd'], dd_df['margin_dd'], color='gray', alpha=0.15, label='未出清杠杆存量剪刀差 (~23%)')
ax3.set_ylabel('累计降幅 (%)', fontsize=12, fontweight='bold')
ax3.set_xlabel('日期', fontsize=12)
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'chart1_deleveraging_vs_price.png'), dpi=200)
plt.close(fig)
print("Saved chart1_deleveraging_vs_price.png")

# -------------------------------------------------------------
# Chart 2: 历史关键暴跌速度横向对比（日均下跌速度 vs 最大回撤）
# -------------------------------------------------------------
res_df = pd.read_csv(os.path.join(output_dir, 'historical_crash_comparison.csv'))

# Select key representative crash episodes
selected_labels = [
    '2026双创: 科创50近期急跌浪',
    '2026双创: 创业板指10月急跌浪',
    '2015股灾: 上证指数第二波暴跌',
    '2015股灾: 创业板指第一波踩踏',
    '2020美股流动性危机: 标普500暴跌',
    '2000科网泡沫: 纳斯达克第一波断崖下杀',
    '2026科技: 科创芯片ETF主跌浪',
    '2026双创: 科创50全波段',
    '2026双创: 创业板指全波段',
    '2008股灾: 上证最快主跌浪',
    '2018美股流动性紧缩: 纳斯达克下杀',
    '2008股灾: 上证综指全周期(6124->1664)',
    '2000科网泡沫: 纳斯达克全周期破裂'
]

chart_df = res_df[res_df['label'].isin(selected_labels)].copy()
chart_df['daily_vel_abs'] = chart_df['daily_velocity_pct'].abs()
chart_df = chart_df.sort_values('daily_vel_abs', ascending=True).reset_index(drop=True)

fig, (ax_bar, ax_scatter) = plt.subplots(1, 2, figsize=(16, 8))

# Horizontal bar chart for daily velocity
bars = ax_bar.barh(chart_df['label'], chart_df['daily_vel_abs'], color='#2b5c8f', alpha=0.85, edgecolor='black')
# Highlight 2026 episodes in distinct red/orange
for i, row in chart_df.iterrows():
    if '2026' in row['label']:
        bars[i].set_color('#d9534f')

ax_bar.set_xlabel('日均下跌速度 (% / 交易日, 绝对值)', fontsize=12, fontweight='bold')
ax_bar.set_title('历史著名暴跌与本波双创的日均下跌速度排行', fontsize=14, fontweight='bold', pad=12)
ax_bar.grid(True, linestyle='--', alpha=0.5, axis='x')

for bar in bars:
    w = bar.get_width()
    ax_bar.text(w + 0.05, bar.get_y() + bar.get_height()/2, f'{w:.2f}%/日', va='center', fontsize=9, fontweight='bold')

# Scatter plot: Total Drop vs Duration
scatter_colors = ['#d9534f' if '2026' in l else '#2b5c8f' for l in chart_df['label']]
ax_scatter.scatter(chart_df['trading_days'], chart_df['total_drop_pct'].abs(), s=chart_df['daily_vel_abs']*120, c=scatter_colors, alpha=0.75, edgecolors='black')

for _, row in chart_df.iterrows():
    offset_y = 1.5
    offset_x = 2
    if '全周期' in row['label']:
        offset_x = -60
    name_short = row['label'].split(':')[-1].strip()
    ax_scatter.annotate(name_short, (row['trading_days'], abs(row['total_drop_pct'])),
                        textcoords="offset points", xytext=(offset_x, offset_y), fontsize=8.5, fontweight='bold')

ax_scatter.set_xlabel('下跌持续交易日 (天)', fontsize=12, fontweight='bold')
ax_scatter.set_ylabel('累计最大跌幅 (% 绝对值)', fontsize=12, fontweight='bold')
ax_scatter.set_title('下跌持续时间 vs 累计跌幅 (气泡大小 = 日均暴跌速度)', fontsize=14, fontweight='bold', pad=12)
ax_scatter.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'chart2_velocity_comparison.png'), dpi=200)
plt.close(fig)
print("Saved chart2_velocity_comparison.png")

# -------------------------------------------------------------
# Chart 3: 国债/黄金异动与流动性抽水传导链条
# -------------------------------------------------------------
df_oct = df_market[df_market['kline_time'] >= '2026-10-01'].copy().sort_values('kline_time').reset_index(drop=True)

fig, axes = plt.subplots(3, 1, figsize=(13, 9), sharex=True)

# 1. 30年国债ETF & 黄金ETF
ax_b = axes[0]
ax_g = ax_b.twinx()
p1, = ax_b.plot(df_oct['kline_time'], df_oct['bond30_etf_close'], color='#2ca02c', lw=2.2, label='30年国债ETF (511090.SH)')
p2, = ax_g.plot(df_oct['kline_time'], df_oct['gold_etf_close'], color='#d4ac0d', lw=2.2, linestyle='--', label='黄金ETF (518880.SH)')
ax_b.set_ylabel('30年国债ETF价格 (元)', color='#2ca02c', fontsize=11, fontweight='bold')
ax_g.set_ylabel('黄金ETF价格 (元)', color='#b7950b', fontsize=11, fontweight='bold')
ax_b.grid(True, linestyle='--', alpha=0.5)
ax_b.set_title('10月流动性抽水异动：30年国债跳水 + 黄金回撤（大机构补仓抗单）', fontsize=13, fontweight='bold')
ax_b.legend([p1, p2], [p1.get_label(), p2.get_label()], loc='upper left')

# Annotate 10-30 breakdown on 30y bond
b_oct30 = df_oct.loc[df_oct['kline_time'] == '2026-10-30', 'bond30_etf_close'].values[0]
ax_b.annotate('琴日30年国债杀跌1点\n流动性终极抵押被抛售', xy=(pd.to_datetime('2026-10-30'), b_oct30),
              xytext=(pd.to_datetime('2026-10-23'), b_oct30 - 0.4),
              arrowprops=dict(facecolor='#2ca02c', shrink=0.05, width=1.2, headwidth=5),
              fontweight='bold', fontsize=9.5, color='#1e8449')

# 2. 通信ETF & 科创芯片ETF
ax_t = axes[1]
ax_c = ax_t.twinx()
p3, = ax_t.plot(df_oct['kline_time'], df_oct['comm_etf_close'], color='#1f77b4', lw=2, label='通信ETF (515880.SH)')
p4, = ax_c.plot(df_oct['kline_time'], df_oct['chip_etf_close'], color='#9467bd', lw=2, linestyle='--', label='科创芯片ETF (588200.SH)')
ax_t.set_ylabel('通信ETF价格 (元)', color='#1f77b4', fontsize=11, fontweight='bold')
ax_c.set_ylabel('科创芯片ETF价格 (元)', color='#9467bd', fontsize=11, fontweight='bold')
ax_t.grid(True, linestyle='--', alpha=0.5)
ax_t.set_title('高杠杆科技主线加速踩踏：通信ETF 与 科创芯片ETF', fontsize=13, fontweight='bold')
ax_t.legend([p3, p4], [p3.get_label(), p4.get_label()], loc='upper right')

# 3. 创业板指 & 科创50
ax_idx = axes[2]
ax_idx2 = ax_idx.twinx()
p5, = ax_idx.plot(df_oct['kline_time'], df_oct['chinext_close'], color='#003f5c', lw=2, label='创业板指')
p6, = ax_idx2.plot(df_oct['kline_time'], df_oct['star50_close'], color='#ff6361', lw=2, linestyle='--', label='科创50')
ax_idx.set_ylabel('创业板指点位', color='#003f5c', fontsize=11, fontweight='bold')
ax_idx2.set_ylabel('科创50点位', color='#ff6361', fontsize=11, fontweight='bold')
ax_idx.grid(True, linestyle='--', alpha=0.5)
ax_idx.set_xlabel('交易日', fontsize=11)
ax_idx.set_title('双创核心宽基指数加速杀跌', fontsize=13, fontweight='bold')
ax_idx.legend([p5, p6], [p5.get_label(), p6.get_label()], loc='upper right')
ax_idx.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'chart3_liquidity_transmission_bonds_gold.png'), dpi=200)
plt.close(fig)
print("Saved chart3_liquidity_transmission_bonds_gold.png")
