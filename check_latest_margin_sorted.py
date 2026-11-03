import sys
import os
import pandas as pd

sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
base = ad.BaseData()
cal = base.get_calendar()

info = ad.InfoData()
ms = info.get_margin_summary(begin_date=20261020, end_date=cal[-1])
ms = ms.sort_values(['TRADE_DATE', 'EXCHANGE']).reset_index(drop=True)
print("Sorted margin summary:")
print(ms.to_string())
