import pandas as pd
import numpy as np

# Load raw klines
df_comm = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_515880.SH.csv')
df_comm['date'] = pd.to_datetime(df_comm['kline_time'])
df_comm = df_comm.sort_values('date').reset_index(drop=True)

df_chip = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_588200.SH.csv')
df_chip['date'] = pd.to_datetime(df_chip['kline_time'])
df_chip = df_chip.sort_values('date').reset_index(drop=True)

# 1. 通信ETF 515880.SH: 2026-07-06 split 1:2 (factor = 2.0 before 2026-07-06)
df_comm['close_adj'] = df_comm['close'].copy()
df_comm.loc[df_comm['date'] < '2026-07-06', 'close_adj'] = df_comm['close'] / 2.0

# 2. 科创芯片 588200.SH: 2026-07-21 split 1:3 (factor = 3.0 before 2026-07-21)
df_chip['close_adj'] = df_chip['close'].copy()
df_chip.loc[df_chip['date'] < '2026-07-21', 'close_adj'] = df_chip['close'] / 3.0

# Save adjusted klines
df_comm.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_515880.SH_adj.csv', index=False)
df_chip.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/kline_588200.SH_adj.csv', index=False)

print("--- 515880.SH Adjusted Prices around Split ---")
print(df_comm[(df_comm['date'] >= '2026-06-25') & (df_comm['date'] <= '2026-07-10')][['date', 'close', 'close_adj']])

print("\n--- 588200.SH Adjusted Prices around Split ---")
print(df_chip[(df_chip['date'] >= '2026-07-15') & (df_chip['date'] <= '2026-07-25')][['date', 'close', 'close_adj']])

# Now compute the exact real drawdowns for both waves:
print("\n=== Real Drawdown Calculations (Split Adjusted) ===")

# Wave 1: 2026-06-25 to 2026-07-31
comm_w1_start = df_comm[df_comm['date'] == '2026-06-25']['close_adj'].values[0]
comm_w1_end = df_comm[df_comm['date'] == '2026-07-31']['close_adj'].values[0]
comm_w1_drop = (comm_w1_end - comm_w1_start) / comm_w1_start * 100

chip_w1_start = df_chip[df_chip['date'] == '2026-06-30']['close_adj'].values[0]
chip_w1_end = df_chip[df_chip['date'] == '2026-07-31']['close_adj'].values[0]
chip_w1_drop = (chip_w1_end - chip_w1_start) / chip_w1_start * 100

print(f"第一波(7月波) 通信ETF复权跌幅: {comm_w1_drop:.2f}% (起点 {comm_w1_start:.4f} -> 终点 {comm_w1_end:.4f})")
print(f"第一波(7月波) 科创芯片复权跌幅: {chip_w1_drop:.2f}% (起点 {chip_w1_start:.4f} -> 终点 {chip_w1_end:.4f})")

# Wave 2: 2026-09-22 to 2026-10-30 (No splits in Wave 2, so raw = adj)
comm_w2_start = df_comm[df_comm['date'] == '2026-09-22']['close_adj'].values[0]
comm_w2_end = df_comm[df_comm['date'] == '2026-10-30']['close_adj'].values[0]
comm_w2_drop = (comm_w2_end - comm_w2_start) / comm_w2_start * 100

chip_w2_start = df_chip[df_chip['date'] == '2026-09-22']['close_adj'].values[0]
chip_w2_end = df_chip[df_chip['date'] == '2026-10-30']['close_adj'].values[0]
chip_w2_drop = (chip_w2_end - chip_w2_start) / chip_w2_start * 100

print(f"第二波(10月波) 通信ETF跌幅: {comm_w2_drop:.2f}% (起点 {comm_w2_start:.4f} -> 终点 {comm_w2_end:.4f})")
print(f"第二波(10月波) 科创芯片跌幅: {chip_w2_drop:.2f}% (起点 {chip_w2_start:.4f} -> 终点 {chip_w2_end:.4f})")

# Full cycle
comm_full_drop = (comm_w2_end - comm_w1_start) / comm_w1_start * 100
chip_full_drop = (chip_w2_end - chip_w1_start) / chip_w1_start * 100
print(f"全周期 通信ETF复权跌幅: {comm_full_drop:.2f}%")
print(f"全周期 科创芯片复权跌幅: {chip_full_drop:.2f}%")
