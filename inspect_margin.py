import sys
import os
import pandas as pd

sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
base = ad.BaseData()
calendar = base.get_calendar()
info = ad.InfoData()

target_etfs = ['515880.SH', '588200.SH', '159995.SZ', '159915.SZ', '588000.SH']
margin_details = info.get_margin_detail(target_etfs, begin_date=20240101, end_date=calendar[-1])

print("Type of margin_details:", type(margin_details))
if isinstance(margin_details, dict):
    for k, v in margin_details.items():
        print(f"Code {k}: shape {v.shape}")
        print(v.tail(5))
        v.to_csv(rf'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/margin_{k}.csv', index=False)
elif isinstance(margin_details, pd.DataFrame):
    print("DataFrame shape:", margin_details.shape)
    margin_details.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/margin_all_targets.csv', index=False)

# Let's also check the raw margin summary for 20261029 and 20261030 by exchange
margin_sum_raw = info.get_margin_summary(begin_date=20261025, end_date=calendar[-1])
print("\nRaw margin summary for recent days:")
print(margin_sum_raw[['TRADE_DATE', 'EXCHANGE', 'SUM_BORROW_MONEY_BALANCE', 'SUM_MARGIN_TRADE_BALANCE']])
