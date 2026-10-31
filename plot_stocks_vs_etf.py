import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

output_dir = r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析'

df_analysis = pd.read_csv(os.path.join(output_dir, 'stocks_vs_etfs_margin_analysis.csv'))
w2_data = df_analysis[df_analysis['波段'].str.contains('第二波')].copy()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# ----------------------------------------------------
# Subplot 1: 通信线（易中天 vs 通信ETF）第二波表现
# ----------------------------------------------------
comm_names = ['新易盛 (300502)', '中际旭创 (300308)', '天孚通信 (300394)', '通信ETF (515880)']
comm_p_drops = [-49.80, -37.26, -41.42, -38.90]
comm_m_drops = [-38.90, -37.26, -26.58, -15.74]

x = np.arange(len(comm_names))
w = 0.35

rects1 = ax1.bar(x - w/2, [abs(v) for v in comm_p_drops], w, label='价格跌幅 (%)', color='#003f5c', alpha=0.9)
rects2 = ax1.bar(x + w/2, [abs(v) for v in comm_m_drops], w, label='融资余额降幅 (%)', color='#ff7c43', alpha=0.9)

ax1.set_xticks(x)
ax1.set_xticklabels(comm_names, rotation=15, fontsize=10, fontweight='bold')
ax1.set_ylabel('变动幅度 (% 绝对值)', fontsize=11, fontweight='bold')
ax1.set_title('通信主线：个股“易中天”同步大去杠杆 vs ETF抗单', fontsize=13, fontweight='bold', pad=12)
ax1.grid(True, linestyle='--', alpha=0.5, axis='y')
ax1.legend(loc='upper right', framealpha=0.9)

for r in rects1:
    h = r.get_height()
    ax1.text(r.get_x() + r.get_width()/2., h + 0.8, f'-{h:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#003f5c')

for r in rects2:
    h = r.get_height()
    ax1.text(r.get_x() + r.get_width()/2., h + 0.8, f'-{h:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#ff7c43')

# ----------------------------------------------------
# Subplot 2: 科创半导体线（寒武纪/中芯/中微 vs 科创芯片ETF）第二波表现
# ----------------------------------------------------
semi_names = ['寒武纪 (688256)', '中芯国际 (688981)', '中微公司 (688012)', '科创芯片ETF (588200)']
semi_p_drops = [-21.50, -20.93, -38.96, -34.93]
semi_m_drops = [-24.36, -14.23, -23.59, 4.41] # ETF actually rose +4.41% !

x2 = np.arange(len(semi_names))
rects3 = ax2.bar(x2 - w/2, [abs(v) for v in semi_p_drops], w, label='价格跌幅 (%)', color='#2f4b7c', alpha=0.9)

# For margin, ETF is positive (+4.41%), stocks are negative
colors_m = ['#d45087' if v < 0 else '#2ca02c' for v in semi_m_drops]
rects4 = ax2.bar(x2 + w/2, semi_m_drops, w, label='融资余额变动 (%)', color=colors_m, alpha=0.9)

ax2.set_xticks(x2)
ax2.set_xticklabels(semi_names, rotation=15, fontsize=10, fontweight='bold')
ax2.set_ylabel('变动幅度 (%)', fontsize=11, fontweight='bold')
ax2.set_title('半导体主线：个股杠杆削减 vs 科创芯片ETF逆势加仓(+4.4%)', fontsize=13, fontweight='bold', pad=12)
ax2.grid(True, linestyle='--', alpha=0.5, axis='y')
ax2.axhline(0, color='black', lw=1)
ax2.legend(loc='upper left', framealpha=0.9)

for r in rects3:
    h = r.get_height()
    ax2.text(r.get_x() + r.get_width()/2., h + 0.8, f'-{h:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2f4b7c')

for i, r in enumerate(rects4):
    h = r.get_height()
    va = 'bottom' if h >= 0 else 'top'
    y_pos = h + 0.8 if h >= 0 else h - 2.5
    txt = f'+{h:.1f}%' if h >= 0 else f'{h:.1f}%'
    ax2.text(r.get_x() + r.get_width()/2., y_pos, txt, ha='center', va=va, fontsize=9, fontweight='bold', color=colors_m[i])

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'chart5_individual_stocks_vs_etf_margin.png'), dpi=200)
plt.close(fig)
print("Saved chart5_individual_stocks_vs_etf_margin.png")
