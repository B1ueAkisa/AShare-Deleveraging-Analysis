import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad
import pandas as pd

config.init_amazing_data()
info = ad.InfoData()

shares = info.get_fund_share(['515880.SH', '588200.SH'], begin_date=20260601, end_date=20261030)
for k, v in shares.items():
    print(f"\n--- Fund share for {k} ---")
    print(v.tail(10))
    v.to_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/share_{k}.csv', index=False)

iopv = info.get_fund_iopv(['515880.SH', '588200.SH'], begin_date=20260601, end_date=20261030)
for k, v in iopv.items():
    print(f"\n--- IOPV for {k} ---")
    print(v.tail(10))
    v.to_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/iopv_{k}.csv', index=False)
