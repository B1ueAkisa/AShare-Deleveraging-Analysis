import sys
import os
import pandas as pd
import numpy as np

sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
base = ad.BaseData()
cal = base.get_calendar()
print("Latest 5 trading calendar dates:", cal[-5:])

info = ad.InfoData()
# Fetch margin summary from 20261015 to latest
ms = info.get_margin_summary(begin_date=20261015, end_date=cal[-1])
print("Margin summary shape:", ms.shape if ms is not None else None)
if ms is not None and len(ms) > 0:
    print(ms.columns.tolist())
    cols = ['TRADE_DATE', 'EXCHANGE', 'SUM_BORROW_MONEY_BALANCE', 'SUM_PURCH_WITH_BORROW_MONEY', 'SUM_REPAYMENT_OF_BORROW_MONEY', 'SUM_MARGIN_TRADE_BALANCE']
    print(ms[cols].tail(15).to_string())
