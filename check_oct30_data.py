import sys
import os
import pandas as pd

sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
base = ad.BaseData()
info = ad.InfoData()

# Check margin summary on 20261030
ms = info.get_margin_summary(begin_date=20261029, end_date=20261031)
print("MS 20261029-20261031:")
print(ms)

# Also check target ETFs margin details on 20261030
target_etfs = ['515880.SH', '588200.SH', '159995.SZ', '159915.SZ', '588000.SH']
try:
    md = info.get_margin_detail(target_etfs, begin_date=20261029, end_date=20261031)
    print("\nTarget ETFs margin detail:")
    print(md)
except Exception as e:
    print("Error fetching detail:", e)

# Also check individual stocks (e.g. 300308.SZ, 300502.SZ, 300394.SZ) on 20261030
target_stocks = ['300308.SZ', '300502.SZ', '300394.SZ', '688256.SH', '688981.SH']
try:
    smd = info.get_margin_detail(target_stocks, begin_date=20261029, end_date=20261031)
    print("\nTarget stocks margin detail:")
    print(smd)
except Exception as e:
    print("Error fetching stock detail:", e)
