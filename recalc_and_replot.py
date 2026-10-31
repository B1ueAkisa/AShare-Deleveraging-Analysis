import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

output_dir = r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析'

# Load market data with adjusted closes
df_market = pd.read_csv(os.path.join(output_dir, 'merged_market_data.csv'))
df_market['kline_time'] = pd.to_datetime(df_market['kline_time'])

df_comm_adj = pd.read_csv(os.path.join(output_dir, 'kline_515880.SH_adj.csv'))[['date', 'close_adj']].rename(columns={'date': 'kline_time', 'close_adj': 'comm_close_adj'})
df_comm_adj['kline_time'] = pd.to_datetime(df_comm_adj['kline_time'])

df_chip_adj = pd.read_csv(os.path.join(output_dir, 'kline_588200.SH_adj.csv'))[['date', 'close_adj']].rename(columns={'date': 'kline_time', 'close_adj': 'chip_close_adj'})
df_chip_adj['kline_time'] = pd.to_datetime(df_chip_adj['kline_time'])

df = pd.merge(df_market, df_comm_adj, on='kline_time', how='left')
df = pd.merge(df, df_chip_adj, on='kline_time', how='left')

# Load margin
df_margin = pd.read_csv(os.path.join(output_dir, 'aggregated_margin_summary.csv'))
df_margin['kline_time'] = pd.to_datetime(df_margin['TRADE_DATE'].astype(str))
df = pd.merge(df, df_margin, on='kline_time', how='left').sort_values('kline_time').reset_index(drop=True)

# Add ETF margin details
m_comm = pd.read_csv(os.path.join(output_dir, 'margin_515880.SH.csv'))
m_comm['kline_time'] = pd.to_datetime(m_comm['TRADE_DATE'].astype(str))
df = pd.merge(df, m_comm[['kline_time', 'BORROW_MONEY_BALANCE']].rename(columns={'BORROW_MONEY_BALANCE': 'comm_margin'}), on='kline_time', how='left')

m_chip = pd.read_csv(os.path.join(output_dir, 'margin_588200.SH.csv'))
m_chip['kline_time'] = pd.to_datetime(m_chip['TRADE_DATE'].astype(str))
df = pd.merge(df, m_chip[['kline_time', 'BORROW_MONEY_BALANCE']].rename(columns={'BORROW_MONEY_BALANCE': 'chip_margin'}), on='kline_time', how='left')

def calc_accurate_wave(df_sub, name):
    start_row = df_sub.iloc[0]
    end_row = df_sub.iloc[-1]
    days = len(df_sub)
    
    # ChiNext
    cy_start, cy_end = start_row['chinext_close'], end_row['chinext_close']
    cy_drop = (cy_end - cy_start) / cy_start * 100
    cy_vel = cy_drop / (days - 1)
    
    # STAR 50
    star_start, star_end = start_row['star50_close'], end_row['star50_close']
    star_drop = (star_end - star_start) / star_start * 100
    star_vel = star_drop / (days - 1)
    
    # Comm ETF (Adjusted)
    comm_start, comm_end = start_row['comm_close_adj'], end_row['comm_close_adj']
    comm_drop = (comm_end - comm_start) / comm_start * 100
    comm_vel = comm_drop / (days - 1)
    
    # Chip ETF (Adjusted)
    chip_start, chip_end = start_row['chip_close_adj'], end_row['chip_close_adj']
    chip_drop = (chip_end - chip_start) / chip_start * 100
    chip_vel = chip_drop / (days - 1)
    
    # Total Margin (using complete day 10-29 if end is 10-30)
    m_start = start_row['SUM_BORROW_MONEY_BALANCE']
    if end_row['kline_time'] == pd.to_datetime('2026-10-30'):
        row_1029 = df_sub[df_sub['kline_time'] == '2026-10-29'].iloc[0]
        m_end = row_1029['SUM_BORROW_MONEY_BALANCE']
    else:
        m_end = end_row['SUM_BORROW_MONEY_BALANCE']
        
    m_drop = (m_end - m_start) / m_start * 100
    m_diff_billion = (m_end - m_start) / 1e8
    
    # Comm Margin
    cm_start = start_row['comm_margin']
    cm_end = end_row['comm_margin']
    cm_drop = (cm_end - cm_start) / cm_start * 100 if pd.notnull(cm_start) and cm_start > 0 else np.nan
    
    # Chip Margin
    chm_start = start_row['chip_margin']
    chm_end = end_row['chip_margin']
    chm_drop = (chm_end - chm_start) / chm_start * 100 if pd.notnull(chm_start) and chm_start > 0 else np.nan
    
    return {
        '波段划分': name,
        '起始日期': start_row['kline_time'].strftime('%Y-%m-%d'),
        '截止日期': end_row['kline_time'].strftime('%Y-%m-%d'),
        '交易天数': days,
        '创业板指跌幅%': round(cy_drop, 2),
        '创业板日均跌速%': round(cy_vel, 2),
        '通信ETF复权跌幅%': round(comm_drop, 2),
        '通信ETF日均跌速%': round(comm_vel, 2),
        '科创50跌幅%': round(star_drop, 2),
        '科创50日均跌速%': round(star_vel, 2),
        '科创芯片复权跌幅%': round(chip_drop, 2),
        '科创芯片日均跌速%': round(chip_vel, 2),
        '全市场融资变化(亿元)': round(m_diff_billion, 1),
        '全市场融资增减%': round(m_drop, 2),
        '通信ETF融资变化%': round(cm_drop, 2),
        '科创芯片融资变化%': round(chm_drop, 2)
    }

w1 = df[(df['kline_time'] >= '2026-06-25') & (df['kline_time'] <= '2026-07-31')]
# Wave 1 for chip specifically starting from its peak 2026-06-30
w1_chip = df[(df['kline_time'] >= '2026-06-30') & (df['kline_time'] <= '2026-07-31')]

w2_rebound = df[(df['kline_time'] >= '2026-09-22') & (df['kline_time'] <= '2026-10-30')]
w2_oct = df[(df['kline_time'] >= '2026-09-30') & (df['kline_time'] <= '2026-10-30')]
w2_late_oct = df[(df['kline_time'] >= '2026-10-23') & (df['kline_time'] <= '2026-10-30')]
w_full = df[(df['kline_time'] >= '2026-06-25') & (df['kline_time'] <= '2026-10-30')]

res_list = [
    calc_accurate_wave(w1, '第一波：7月完整出清波 (06.25 - 07.31)'),
    calc_accurate_wave(w2_rebound, '第二波：9月高点至10月底主跌浪 (09.22 - 10.30)'),
    calc_accurate_wave(w2_oct, '第二波：国庆节后流动性收紧波 (09.30 - 10.30)'),
    calc_accurate_wave(w2_late_oct, '第二波极速冲刺：10月下旬踩踏浪 (10.23 - 10.30)'),
    calc_accurate_wave(w_full, '全波段回顾：6月底峰值至10月底 (06.25 - 10.30)')
]

df_res_table = pd.DataFrame(res_list)
df_res_table.to_csv(os.path.join(output_dir, 'two_waves_comparison.csv'), index=False)
print("=== 更新后：两波下跌复权精准对比矩阵 ===")
print(df_res_table.to_string())

# Re-render Chart 4
w1_df = df[(df['kline_time'] >= '2026-06-25') & (df['kline_time'] <= '2026-07-31')].copy().reset_index(drop=True)
w2_df = df[(df['kline_time'] >= '2026-09-22') & (df['kline_time'] <= '2026-10-30')].copy().reset_index(drop=True)

for col in ['chinext_close', 'star50_close', 'comm_close_adj', 'chip_close_adj']:
    w1_df[f'{col}_norm'] = w1_df[col] / w1_df[col].iloc[0] * 100
    w2_df[f'{col}_norm'] = w2_df[col] / w2_df[col].iloc[0] * 100

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Panel 1: Normalized Overlay (Trading Days elapsed)
ax_p1 = axes[0]
ax_p1.plot(w1_df.index, w1_df['comm_close_adj_norm'], label='第一波(7月): 通信ETF复权 (-38.2%)', color='#1f77b4', lw=2, linestyle='--')
ax_p1.plot(w1_df.index, w1_df['chip_close_adj_norm'], label='第一波(7月): 科创芯片复权 (-32.2%)', color='#ff7f0e', lw=2, linestyle='--')
ax_p1.plot(w2_df.index, w2_df['comm_close_adj_norm'], label='第二波(10月): 通信ETF (-38.9%)', color='#003f5c', lw=2.5)
ax_p1.plot(w2_df.index, w2_df['chip_close_adj_norm'], label='第二波(10月): 科创芯片 (-34.9%)', color='#d45087', lw=2.5)
ax_p1.plot(w2_df.index, w2_df['chinext_close_norm'], label='第二波(10月): 创业板指 (-29.0%)', color='#7a5195', lw=1.5, linestyle='-.')
ax_p1.plot(w2_df.index, w2_df['star50_close_norm'], label='第二波(10月): 科创50 (-30.3%)', color='#f95d6a', lw=1.5, linestyle='-.')

ax_p1.set_xlabel('经历交易日数 (天)', fontsize=11, fontweight='bold')
ax_p1.set_ylabel('复权归一点位 (起点=100)', fontsize=11, fontweight='bold')
ax_p1.set_title('第一波(7月) vs 第二波(10月) 复权走势轨迹重叠', fontsize=13, fontweight='bold')
ax_p1.grid(True, linestyle='--', alpha=0.5)
ax_p1.legend(loc='lower left', fontsize=8.5, framealpha=0.9)

# Panel 2: Deleveraging vs Drawdown Scissors Gap
ax_p2 = axes[1]
waves_labels = ['第一波 (7月出清波)', '第二波 (10月收紧波)']
index_drops = [23.51, 29.01] # ChiNext
margin_drops = [13.99, 10.27] # Total Margin
chip_etf_drops = [32.23, 34.93] # Chip ETF (Adjusted!)
comm_etf_drops = [38.18, 38.90] # Comm ETF (Adjusted!)

x = np.arange(len(waves_labels))
width = 0.2

b1 = ax_p2.bar(x - 1.5*width, index_drops, width, label='创业板指跌幅 (%)', color='#003f5c')
b2 = ax_p2.bar(x - 0.5*width, comm_etf_drops, width, label='通信ETF复权跌幅 (%)', color='#2f4b7c')
b3 = ax_p2.bar(x + 0.5*width, chip_etf_drops, width, label='科创芯片复权跌幅 (%)', color='#f95d6a')
b4 = ax_p2.bar(x + 1.5*width, margin_drops, width, label='全市场融资去化 (%)', color='#ff7c43')

ax_p2.set_xticks(x)
ax_p2.set_xticklabels(waves_labels, fontsize=11, fontweight='bold')
ax_p2.set_ylabel('变动幅度 (% 绝对值)', fontsize=11, fontweight='bold')
ax_p2.set_title('两波真实复权跌幅 vs 杠杆去化剪刀差', fontsize=13, fontweight='bold')
ax_p2.grid(True, linestyle='--', alpha=0.5, axis='y')
ax_p2.legend(loc='upper right', fontsize=8.5, framealpha=0.9)

for bar in b1 + b2 + b3 + b4:
    h = bar.get_height()
    ax_p2.text(bar.get_x() + bar.get_width()/2., h + 0.8, f'{h:.1f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

# Panel 3: Velocity Comparison
ax_p3 = axes[2]
episodes = [
    '第一波: 创业板指 (7月)',
    '第一波: 科创芯片复权 (7月)',
    '第一波: 通信ETF复权 (7月)',
    '第二波: 创业板指 (10月)',
    '第二波: 科创芯片 (10月)',
    '第二波: 通信ETF (10月)',
    '10月下旬急跌: 科创50',
    '10月下旬急跌: 科创芯片',
    '10月下旬急跌: 通信ETF'
]
vels = [0.90, 1.47, 1.47, 1.32, 1.59, 1.77, 2.75, 3.19, 3.19]
colors = ['#1f77b4', '#3274a1', '#285e82', '#003f5c', '#d45087', '#f95d6a', '#d9534f', '#a00000', '#7b0000']

bars_vel = ax_p3.barh(episodes, vels, color=colors, alpha=0.85, edgecolor='black')
ax_p3.set_xlabel('日均下跌速度 (% / 交易日)', fontsize=11, fontweight='bold')
ax_p3.set_title('复权日均跌速对比：第二波冲刺显著超越第一波', fontsize=13, fontweight='bold')
ax_p3.grid(True, linestyle='--', alpha=0.5, axis='x')

for b in bars_vel:
    w = b.get_width()
    ax_p3.text(w + 0.05, b.get_y() + b.get_height()/2, f'{w:.2f}%/日', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'chart4_two_waves_deep_dive.png'), dpi=200)
plt.close(fig)
print("Re-rendered chart4_two_waves_deep_dive.png with adjusted ETF prices!")
