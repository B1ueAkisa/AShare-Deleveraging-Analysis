import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set font for Chinese display
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 11), dpi=150)
fig.suptitle('2026年11月3日科技避难所决堤与全线强平全景复盘\n(The Reservoir Breach: Tech ETF Refuge Collapse & Margin Liquidation)', 
             fontsize=16, fontweight='bold', y=0.98)

# 1. 2026-11-03 核心资产单日跌幅榜
assets = [
    ('天孚通信', -12.80, '#d62728'),
    ('中际旭创', -12.69, '#d62728'),
    ('罗博特科', -11.48, '#d62728'),
    ('寒武纪-U', -10.81, '#d62728'),
    ('生益科技(跌停)', -10.00, '#e377c2'),
    ('兴森科技(跌停)', -10.01, '#e377c2'),
    ('德明利(跌停)', -10.00, '#e377c2'),
    ('剑桥科技', -9.53, '#d62728'),
    ('新易盛', -9.46, '#d62728'),
    ('胜宏科技', -9.12, '#d62728'),
    ('通信ETF (515880)', -7.36, '#ff7f0e'),
    ('科创半导 (588170)', -6.16, '#ff7f0e'),
    ('半导设备 (560780)', -5.73, '#ff7f0e'),
    ('科创芯片 (588200)', -5.16, '#ff7f0e'),
    ('芯片ETF (512760)', -4.52, '#ff7f0e'),
    ('科创50 ETF (588000)', -3.79, '#1f77b4'),
    ('30年国债ETF (511090)', 0.60, '#2ca02c'),
    ('黄金ETF (518880)', 0.60, '#bcbd22'),
]

names = [x[0] for x in assets][::-1]
pcts = [x[1] for x in assets][::-1]
colors = [x[2] for x in assets][::-1]

bars = ax1.barh(names, pcts, color=colors, alpha=0.85, edgecolor='black', linewidth=0.5)
ax1.set_title('11月3日单日涨跌幅分布 (%)：科技无差别踩踏 vs 国债黄金避险', fontsize=12, fontweight='bold')
ax1.set_xlabel('单日涨跌幅 (%)', fontsize=10)
ax1.axvline(0, color='black', linestyle='--', linewidth=0.8)
ax1.grid(axis='x', linestyle=':', alpha=0.6)
for bar in bars:
    w = bar.get_width()
    ax1.text(w + (0.3 if w >= 0 else -0.3), bar.get_y() + bar.get_height()/2, 
             f"{w:+.2f}%", ha='left' if w >= 0 else 'right', va='center', fontsize=8, fontweight='bold')

# 2. 累计跌幅对比：历史极值 vs 第二波
stocks_drawdown = [
    ('新易盛', -78.82, -63.50),
    ('天孚通信', -76.46, -57.68),
    ('胜宏科技', -67.85, -51.31),
    ('中际旭创', -66.11, -50.75),
    ('通信ETF', -57.31, -44.64),
    ('科创芯片', -55.49, -38.70),
    ('寒武纪-U', -52.60, -33.50),
    ('科创半导', -48.20, -44.06),
]

names_dd = [x[0] for x in stocks_drawdown]
total_dd = [x[1] for x in stocks_drawdown]
wave2_dd = [x[2] for x in stocks_drawdown]

x = np.arange(len(names_dd))
width = 0.35

rects1 = ax2.bar(x - width/2, total_dd, width, label='历史总跌幅 (距6月顶)', color='#8c564b', alpha=0.85, edgecolor='black', linewidth=0.5)
rects2 = ax2.bar(x + width/2, wave2_dd, width, label='第二波跌幅 (距9月22日反弹顶)', color='#d62728', alpha=0.85, edgecolor='black', linewidth=0.5)

ax2.set_title('全周期累计最大回撤 (%)：个股跌去3/4，ETF腰斩', fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(names_dd, rotation=25, fontsize=9)
ax2.set_ylabel('累计回撤 (%)', fontsize=10)
ax2.grid(axis='y', linestyle=':', alpha=0.6)
ax2.legend(loc='lower left', fontsize=9)

for rect in rects1:
    h = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2, h - 2, f"{h:.1f}%", ha='center', va='top', fontsize=8, color='#5c2a22')
for rect in rects2:
    h = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2, h - 2, f"{h:.1f}%", ha='center', va='top', fontsize=8, color='#8a1515')

# 3. 避难所陷阱：科创50 ETF与通信ETF融资余额在暴跌前夕冲顶
df_588000 = pd.read_csv('margin_588000.SH.csv')
df_588000['TRADE_DATE'] = df_588000['TRADE_DATE'].astype(str)
df_sub = df_588000[df_588000['TRADE_DATE'] >= '20260601'].sort_values('TRADE_DATE').copy()
col_margin = 'BORROW_MONEY_BALANCE' if 'BORROW_MONEY_BALANCE' in df_sub.columns else 'MARGIN_BALANCE'
df_sub['MARGIN_BALANCE_100M'] = df_sub[col_margin] / 1e8

# Add 20261102 data point
if '20261102' not in df_sub['TRADE_DATE'].values:
    row_nov02 = pd.DataFrame([{'TRADE_DATE': '20261102', 'MARGIN_BALANCE_100M': 50.77}])
    df_sub = pd.concat([df_sub, row_nov02], ignore_index=True)

ax3_2 = ax3.twinx()
p1 = ax3.plot(pd.to_datetime(df_sub['TRADE_DATE']), df_sub['MARGIN_BALANCE_100M'], color='#1f77b4', linewidth=2.5, label='科创50ETF 融资余额(亿元)')
ax3.scatter(pd.to_datetime(df_sub['TRADE_DATE'].iloc[-1]), df_sub['MARGIN_BALANCE_100M'].iloc[-1], color='red', s=60, zorder=5)
ax3.annotate(f"11-02 历史最高峰\n{df_sub['MARGIN_BALANCE_100M'].iloc[-1]:.2f} 亿元", 
             (pd.to_datetime(df_sub['TRADE_DATE'].iloc[-1]), df_sub['MARGIN_BALANCE_100M'].iloc[-1]),
             textcoords="offset points", xytext=(-70,-20), ha='center', fontsize=9, fontweight='bold', color='red',
             arrowprops=dict(arrowstyle='->', color='red', lw=1.2))

# 通信 ETF 融资余额
df_515880 = pd.read_csv('margin_515880.SH.csv')
df_515880['TRADE_DATE'] = df_515880['TRADE_DATE'].astype(str)
df_sub_515880 = df_515880[df_515880['TRADE_DATE'] >= '20260601'].sort_values('TRADE_DATE').copy()
col_margin_515 = 'BORROW_MONEY_BALANCE' if 'BORROW_MONEY_BALANCE' in df_sub_515880.columns else 'MARGIN_BALANCE'
df_sub_515880['MARGIN_BALANCE_100M'] = df_sub_515880[col_margin_515] / 1e8
if '20261102' not in df_sub_515880['TRADE_DATE'].values:
    row_nov02_515 = pd.DataFrame([{'TRADE_DATE': '20261102', 'MARGIN_BALANCE_100M': 10.75}])
    df_sub_515880 = pd.concat([df_sub_515880, row_nov02_515], ignore_index=True)

p2 = ax3_2.plot(pd.to_datetime(df_sub_515880['TRADE_DATE']), df_sub_515880['MARGIN_BALANCE_100M'], color='#ff7f0e', linestyle='--', linewidth=2, label='通信ETF 融资余额(亿元)')

ax3.set_title('“避难所陷阱”：双创ETF融资余额在11月2日冲顶，随后决堤', fontsize=12, fontweight='bold')
ax3.set_ylabel('科创50ETF 融资余额 (亿元)', color='#1f77b4', fontsize=10)
ax3_2.set_ylabel('通信ETF 融资余额 (亿元)', color='#ff7f0e', fontsize=10)
ax3.grid(True, linestyle=':', alpha=0.6)

lines = p1 + p2
labels = [l.get_label() for l in lines]
ax3.legend(lines, labels, loc='upper left', fontsize=9)

# 4. 终极避险：30年国债ETF vs 通信ETF走势对比
df_bond = pd.read_csv('kline_511090.SH.csv')
col_date_bond = 'kline_time' if 'kline_time' in df_bond.columns else 'trade_date'
df_bond['date_clean'] = pd.to_datetime(df_bond[col_date_bond])
df_bond = df_bond[df_bond['date_clean'] >= '2026-06-01'].sort_values('date_clean').copy()
# Add 11-02 and 11-03
rows_bond_new = pd.DataFrame([
    {'date_clean': pd.to_datetime('2026-11-02'), 'close': 120.59},
    {'date_clean': pd.to_datetime('2026-11-03'), 'close': 121.31}
])
df_bond = pd.concat([df_bond, rows_bond_new], ignore_index=True)
df_bond['close_norm'] = df_bond['close'] / df_bond['close'].iloc[0] * 100

df_tech_adj = pd.read_csv('kline_515880.SH_adj.csv')
col_date_tech = 'date' if 'date' in df_tech_adj.columns else 'kline_time'
df_tech_adj['date_clean'] = pd.to_datetime(df_tech_adj[col_date_tech])
df_tech_adj = df_tech_adj[df_tech_adj['date_clean'] >= '2026-06-01'].sort_values('date_clean').copy()
rows_tech_new = pd.DataFrame([
    {'date_clean': pd.to_datetime('2026-11-02'), 'close_adj': 0.435},
    {'date_clean': pd.to_datetime('2026-11-03'), 'close_adj': 0.403}
])
df_tech_adj = pd.concat([df_tech_adj, rows_tech_new], ignore_index=True)
df_tech_adj['close_norm'] = df_tech_adj['close_adj'] / df_tech_adj['close_adj'].iloc[0] * 100

ax4.plot(df_tech_adj['date_clean'], df_tech_adj['close_norm'], color='#d62728', linewidth=2, label='通信ETF (前复权, 2026-06=100)')
ax4_2 = ax4.twinx()
ax4_2.plot(df_bond['date_clean'], df_bond['close_norm'], color='#2ca02c', linewidth=2.5, label='30年国债ETF (2026-06=100)')

ax4.set_title('资金终极流向：科技杠杆爆仓清盘 -> 涌入30年超长国债避险', fontsize=12, fontweight='bold')
ax4.set_ylabel('通信ETF 归一化净值', color='#d62728', fontsize=10)
ax4_2.set_ylabel('30年国债ETF 归一化净值', color='#2ca02c', fontsize=10)
ax4.grid(True, linestyle=':', alpha=0.6)

lines1, labels1 = ax4.get_legend_handles_labels()
lines2, labels2 = ax4_2.get_legend_handles_labels()
ax4.legend(lines1 + lines2, labels1 + labels2, loc='center left', fontsize=9)

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig('chart7_reservoir_breach_nov03.png', dpi=200)
print("Chart 7 generated successfully: chart7_reservoir_breach_nov03.png")
