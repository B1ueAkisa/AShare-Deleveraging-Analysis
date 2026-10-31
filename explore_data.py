import sys
import os

# Add 星耀数智 to sys.path to import config
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad
import pandas as pd

print("Logging into AmazingData...")
config.init_amazing_data()

base = ad.BaseData()
calendar = base.get_calendar()
print(f"Calendar range: {calendar[0]} to {calendar[-1]}, total {len(calendar)} days")

info = ad.InfoData()
print("\nFetching margin summary...")
try:
    margin_sum = info.get_margin_summary(begin_date=20240101, end_date=calendar[-1])
    print(f"Margin summary shape: {margin_sum.shape if margin_sum is not None else None}")
    if margin_sum is not None:
        print("Margin summary head/tail:")
        print(margin_sum.tail(10))
except Exception as e:
    print(f"Error fetching margin summary: {e}")

# Check treasury yield
try:
    print("\nFetching treasury yield...")
    ty = info.get_treasury_yield(begin_date=20260101, end_date=calendar[-1])
    print(f"Treasury yield shape: {ty.shape if ty is not None else None}")
    if ty is not None:
        print(ty.tail(5))
except Exception as e:
    print(f"Error fetching treasury yield: {e}")
