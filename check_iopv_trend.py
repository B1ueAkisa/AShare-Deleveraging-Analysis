import pandas as pd
import numpy as np

# Load IOPV
iopv_comm = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/iopv_515880.SH.csv')
iopv_comm['date'] = pd.to_datetime(iopv_comm['PRICE_DATE'].astype(str))
iopv_comm = iopv_comm.sort_values('date').reset_index(drop=True)

iopv_chip = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/iopv_588200.SH.csv')
iopv_chip['date'] = pd.to_datetime(iopv_chip['PRICE_DATE'].astype(str))
iopv_chip = iopv_chip.sort_values('date').reset_index(drop=True)

print("--- IOPV Comm sample (June to July) ---")
print(iopv_comm[(iopv_comm['date'] >= '2026-06-20') & (iopv_comm['date'] <= '2026-07-31')].head(15))
print(iopv_comm[(iopv_comm['date'] >= '2026-06-20') & (iopv_comm['date'] <= '2026-07-31')].tail(10))

print("\n--- IOPV Chip sample (June to July) ---")
print(iopv_chip[(iopv_chip['date'] >= '2026-06-20') & (iopv_chip['date'] <= '2026-07-31')].head(15))
print(iopv_chip[(iopv_chip['date'] >= '2026-06-20') & (iopv_chip['date'] <= '2026-07-31')].tail(10))
